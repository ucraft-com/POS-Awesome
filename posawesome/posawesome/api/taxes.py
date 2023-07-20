# -*- coding: utf-8 -*-
# Copyright (c) 2023, Youssef Restom and contributors
# For license information, please see license.txt


from __future__ import unicode_literals

# import frappe
import json
from frappe import _
from frappe.utils import flt, cint, nowdate


def calculate_taxes(invoice_doc):
    invoice_doc.transaction_date = nowdate()
    rounding_adjustment_computed = invoice_doc.get(
        "is_consolidated"
    ) and invoice_doc.get("rounding_adjustment")
    if not rounding_adjustment_computed:
        invoice_doc.rounding_adjustment = 0

    # maintain actual tax rate based on idx
    actual_tax_dict = dict(
        [
            [tax.idx, flt(tax.tax_amount, tax.precision("tax_amount"))]
            for tax in invoice_doc.get("taxes")
            if tax.charge_type == "Actual"
        ]
    )

    for tax in invoice_doc.get("taxes"):
        if not (invoice_doc.get("is_consolidated") or tax.get("dont_recompute_tax")):
            tax.item_wise_tax_detail = {}
        tax.tax_amount = 0.0
        tax.tax_amount_after_discount_amount = 0.0

    discount_amount_applied = False
    if invoice_doc.apply_discount_on == "Grand Total" and invoice_doc.get(
        "is_cash_or_non_trade_discount"
    ):
        discount_amount_applied = True

    for n, item in enumerate(invoice_doc.items):
        item.net_amount = item.amount
        item_tax_map = _load_item_tax_rate(item.item_tax_rate)

        for i, tax in enumerate(invoice_doc.get("taxes")):
            # tax_amount represents the amount of tax for the current step
            current_tax_amount = get_current_tax_amount(
                invoice_doc, item, tax, item_tax_map
            )

            # Adjust divisional loss to the last item
            if tax.charge_type == "Actual":
                actual_tax_dict[tax.idx] -= current_tax_amount
                if n == len(invoice_doc.items) - 1:
                    current_tax_amount += actual_tax_dict[tax.idx]

            # accumulate tax amount into tax.tax_amount
            if tax.charge_type != "Actual" and not (
                discount_amount_applied
                and invoice_doc.apply_discount_on == "Grand Total"
            ):
                tax.tax_amount += current_tax_amount

            # store tax_amount for current item as it will be used for
            # charge type = 'On Previous Row Amount'
            tax.tax_amount_for_current_item = current_tax_amount

            # set tax after discount
            tax.tax_amount_after_discount_amount += current_tax_amount

            current_tax_amount = get_tax_amount_if_for_valuation_or_deduction(
                invoice_doc, current_tax_amount, tax
            )

            # note: grand_total_for_current_item contains the contribution of
            # item's amount, previously applied tax and the current tax on that item
            if i == 0:
                tax.grand_total_for_current_item = flt(
                    item.net_amount + current_tax_amount
                )
            else:
                tax.grand_total_for_current_item = flt(
                    invoice_doc.get("taxes")[i - 1].grand_total_for_current_item
                    + current_tax_amount
                )

    for tax in invoice_doc.get("taxes"):
        tax.dont_recompute_tax = 1
        tax.item_wise_tax_detail = json.dumps(tax.item_wise_tax_detail)


def _load_item_tax_rate(item_tax_rate):
    return json.loads(item_tax_rate) if item_tax_rate else {}


def _get_tax_rate(invoice_doc, tax, item_tax_map):
    if tax.account_head in item_tax_map:
        return flt(
            item_tax_map.get(tax.account_head), invoice_doc.precision("rate", tax)
        )
    else:
        return 0.0


def set_item_wise_tax(invoice_doc, item, tax, tax_rate, current_tax_amount):
    # store tax breakup for each item
    key = item.item_code or item.item_name
    item_wise_tax_amount = current_tax_amount * invoice_doc.conversion_rate
    if (
        tax.item_wise_tax_detail.get(key)
        and tax.item_wise_tax_detail.get(key)[0] == tax_rate
    ):
        item_wise_tax_amount += tax.item_wise_tax_detail[key][1]

    elif not tax.item_wise_tax_detail.get(key):
        tax.item_wise_tax_detail[key] = [tax_rate, flt(item_wise_tax_amount)]


def get_current_tax_amount(invoice_doc, item, tax, item_tax_map):
    tax_rate = _get_tax_rate(invoice_doc, tax, item_tax_map)
    current_tax_amount = 0.0

    if tax.charge_type == "Actual":
        # distribute the tax amount proportionally to each item row
        actual = flt(tax.tax_amount, tax.precision("tax_amount"))
        current_tax_amount = (
            item.net_amount * actual / invoice_doc.doc.net_total
            if invoice_doc.net_total
            else 0.0
        )

    elif tax.charge_type == "On Net Total":
        current_tax_amount = (tax_rate / 100.0) * item.net_amount
    elif tax.charge_type == "On Previous Row Amount":
        current_tax_amount = (tax_rate / 100.0) * invoice_doc.get("taxes")[
            cint(tax.row_id) - 1
        ].tax_amount_for_current_item
    elif tax.charge_type == "On Previous Row Total":
        current_tax_amount = (tax_rate / 100.0) * invoice_doc.get("taxes")[
            cint(tax.row_id) - 1
        ].grand_total_for_current_item
    elif tax.charge_type == "On Item Quantity":
        current_tax_amount = tax_rate * item.qty

    if not (invoice_doc.get("is_consolidated") or tax.get("dont_recompute_tax")):
        set_item_wise_tax(invoice_doc, item, tax, tax_rate, current_tax_amount)

    return current_tax_amount


def get_tax_amount_if_for_valuation_or_deduction(invoice_doc, tax_amount, tax):
    # if just for valuation, do not add the tax amount in total
    # if tax/charges is for deduction, multiply by -1
    if getattr(tax, "category", None):
        tax_amount = 0.0 if (tax.category == "Valuation") else tax_amount
        if invoice_doc.doctype in [
            "Purchase Order",
            "Purchase Invoice",
            "Purchase Receipt",
            "Supplier Quotation",
        ]:
            tax_amount *= -1.0 if (tax.add_deduct_tax == "Deduct") else 1.0
    return tax_amount
