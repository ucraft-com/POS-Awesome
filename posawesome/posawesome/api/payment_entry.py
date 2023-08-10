# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe, erpnext, json
from frappe import _
from frappe.utils import nowdate, getdate, flt
from erpnext.accounts.party import get_party_account
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.doctype.journal_entry.journal_entry import (
    get_default_bank_cash_account,
)
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.doctype.bank_account.bank_account import get_party_bank_account
from posawesome.posawesome.api.m_pesa import submit_mpesa_payment
from erpnext.accounts.utils import QueryPaymentLedger, get_outstanding_invoices as _get_outstanding_invoices


def create_payment_entry(
    company,
    customer,
    amount,
    currency,
    mode_of_payment,
    reference_date=None,
    reference_no=None,
    posting_date=None,
    cost_center=None,
    submit=0,
):
    # TODO : need to have a better way to handle currency
    date = nowdate() if not posting_date else posting_date
    party_type = "Customer"
    party_account = get_party_account(party_type, customer, company)
    party_account_currency = get_account_currency(party_account)
    if party_account_currency != currency:
        frappe.throw(
            _(
                "Currency is not correct, party account currency is {party_account_currency} and transaction currency is {currency}"
            ).format(party_account_currency=party_account_currency, currency=currency)
        )
    payment_type = "Receive"

    bank = get_bank_cash_account(company, mode_of_payment)
    company_currency = frappe.get_value("Company", company, "default_currency")
    conversion_rate = get_exchange_rate(currency, company_currency, date, "for_selling")
    paid_amount, received_amount = set_paid_amount_and_received_amount(
        party_account_currency, bank, amount, payment_type, None, conversion_rate
    )

    pe = frappe.new_doc("Payment Entry")
    pe.payment_type = payment_type
    pe.company = company
    pe.cost_center = cost_center or erpnext.get_default_cost_center(company)
    pe.posting_date = date
    pe.mode_of_payment = mode_of_payment
    pe.party_type = party_type
    pe.party = customer

    pe.paid_from = party_account if payment_type == "Receive" else bank.account
    pe.paid_to = party_account if payment_type == "Pay" else bank.account
    pe.paid_from_account_currency = (
        party_account_currency if payment_type == "Receive" else bank.account_currency
    )
    pe.paid_to_account_currency = (
        party_account_currency if payment_type == "Pay" else bank.account_currency
    )
    pe.paid_amount = paid_amount
    pe.received_amount = received_amount
    pe.letter_head = frappe.get_value("Company", company, "default_letter_head")
    pe.reference_date = reference_date
    pe.reference_no = reference_no
    if pe.party_type in ["Customer", "Supplier"]:
        bank_account = get_party_bank_account(pe.party_type, pe.party)
        pe.set("bank_account", bank_account)
        pe.set_bank_account_data()

    pe.setup_party_account_field()
    pe.set_missing_values()

    if party_account and bank:
        pe.set_amounts()
    if submit:
        pe.docstatus = 1
    pe.insert(ignore_permissions=True)
    return pe


def get_bank_cash_account(company, mode_of_payment, bank_account=None):
    bank = get_default_bank_cash_account(
        company, "Bank", mode_of_payment=mode_of_payment, account=bank_account
    )

    if not bank:
        bank = get_default_bank_cash_account(
            company, "Cash", mode_of_payment=mode_of_payment, account=bank_account
        )

    return bank


def set_paid_amount_and_received_amount(
    party_account_currency,
    bank,
    outstanding_amount,
    payment_type,
    bank_amount,
    conversion_rate,
):
    paid_amount = received_amount = 0
    if party_account_currency == bank.account_currency:
        paid_amount = received_amount = abs(outstanding_amount)
    elif payment_type == "Receive":
        paid_amount = abs(outstanding_amount)
        if bank_amount:
            received_amount = bank_amount
        else:
            received_amount = paid_amount * conversion_rate

    else:
        received_amount = abs(outstanding_amount)
        if bank_amount:
            paid_amount = bank_amount
        else:
            # if party account currency and bank currency is different then populate paid amount as well
            paid_amount = received_amount * conversion_rate

    return paid_amount, received_amount


@frappe.whitelist()
def get_outstanding_invoices(company, currency, customer=None, pos_profile_name=None):
    if customer:
        precision = frappe.get_precision("Sales Invoice", "outstanding_amount") or 2
        outstanding_invoices = _get_outstanding_invoices(
            party_type="Customer",
            party=customer,
            account=get_party_account("Customer", customer, company),
        )
        invoices_list = []
        customer_name = frappe.get_cached_value("Customer", customer, "customer_name")
        for invoice in outstanding_invoices:
            if invoice.get("currency") == currency:
                if pos_profile_name and frappe.get_cached_value(
                    "Sales Invoice", invoice.get("voucher_no"), "pos_profile"
                ) != pos_profile_name:
                    continue
                outstanding_amount = invoice.outstanding_amount
                if outstanding_amount > 0.5 / (10**precision):
                    invoice_dict = {
                        "name": invoice.get("voucher_no"),
                        "customer": customer,
                        "customer_name": customer_name,
                        "outstanding_amount": invoice.get("outstanding_amount"),
                        "grand_total": invoice.get("invoice_amount"),
                        "due_date": invoice.get("due_date"),
                        "posting_date": invoice.get("posting_date"),
                        "currency": invoice.get("currency"),
                        "pos_profile": pos_profile_name,

                    }
                    invoices_list.append(invoice_dict)
        return invoices_list
    else:
        filters = {
            "company": company,
            "outstanding_amount": (">", 0),
            "docstatus": 1,
            "is_return": 0,
            "currency": currency,
        }
        if customer:
            filters.update({"customer": customer})
        if pos_profile_name:
            filters.update({"pos_profile": pos_profile_name})
        invoices = frappe.get_all(
            "Sales Invoice",
            filters=filters,
            fields=[
                "name",
                "customer",
                "customer_name",
                "outstanding_amount",
                "grand_total",
                "due_date",
                "posting_date",
                "currency",
                "pos_profile",
            ],
            order_by="due_date asc",
        )
        return invoices


@frappe.whitelist()
def get_unallocated_payments(customer, company, currency, mode_of_payment=None):
    filters = {
        "party": customer,
        "company": company,
        "docstatus": 1,
        "party_type": "Customer",
        "payment_type": "Receive",
        "unallocated_amount": [">", 0],
        "paid_from_account_currency": currency,
    }
    if mode_of_payment:
        filters.update({"mode_of_payment": mode_of_payment})
    unallocated_payment = frappe.get_all(
        "Payment Entry",
        filters=filters,
        fields=[
            "name",
            "paid_amount",
            "party_name as customer_name",
            "received_amount",
            "posting_date",
            "unallocated_amount",
            "mode_of_payment",
            "paid_from_account_currency as currency",
        ],
        order_by="posting_date asc",
    )
    return unallocated_payment


@frappe.whitelist()
def process_pos_payment(payload):
    data = json.loads(payload)
    data = frappe._dict(data)
    if not data.pos_profile.get("posa_use_pos_awesome_payments"):
        frappe.throw(_("POS Awesome Payments is not enabled for this POS Profile"))

    # validate data
    if not data.customer:
        frappe.throw(_("Customer is required"))
    if not data.company:
        frappe.throw(_("Company is required"))
    if not data.currency:
        frappe.throw(_("Currency is required"))
    if not data.pos_profile_name:
        frappe.throw(_("POS Profile is required"))
    if not data.pos_opening_shift_name:
        frappe.throw(_("POS Opening Shift is required"))

    company = data.company
    currency = data.currency
    customer = data.customer
    pos_opening_shift_name = data.pos_opening_shift_name
    allow_make_new_payments = data.pos_profile.get("posa_allow_make_new_payments")
    allow_reconcile_payments = data.pos_profile.get("posa_allow_reconcile_payments")
    allow_mpesa_reconcile_payments = data.pos_profile.get(
        "posa_allow_mpesa_reconcile_payments"
    )
    today = nowdate()

    new_payments_entry = []
    all_payments_entry = []
    errors = []
    reconcile_doc = None

    # first process mpesa payments
    if (
        allow_mpesa_reconcile_payments
        and len(data.selected_mpesa_payments) > 0
        and data.total_selected_mpesa_payments > 0
    ):
        for mpesa_payment in data.selected_mpesa_payments:
            try:
                new_mpesa_payment = submit_mpesa_payment(
                    mpesa_payment.get("name"), customer
                )
                new_payments_entry.append(new_mpesa_payment)
                all_payments_entry.append(new_mpesa_payment)
            except Exception as e:
                errors.append(e)

    # then process the new payments
    if (
        allow_make_new_payments
        and len(data.payment_methods) > 0
        and data.total_payment_methods > 0
    ):
        for payment_method in data.payment_methods:
            try:
                if not payment_method.get("amount"):
                    continue
                new_payment_entry = create_payment_entry(
                    company=company,
                    customer=customer,
                    currency=currency,
                    amount=flt(payment_method.get("amount")),
                    mode_of_payment=payment_method.get("mode_of_payment"),
                    posting_date=today,
                    reference_no=pos_opening_shift_name,
                    reference_date=today,
                    cost_center=data.pos_profile.get("cost_center"),
                    submit=1,
                )
                new_payments_entry.append(new_payment_entry)
                all_payments_entry.append(new_payment_entry)
            except Exception as e:
                errors.append(e)

    # then then reconcile the new payments and the unallocated payments with the outstanding invoices
    if len(data.selected_invoices) > 0 and data.total_selected_invoices > 0:
        if (
            allow_reconcile_payments
            and len(data.selected_payments) > 0
            and data.total_selected_payments > 0
        ):
            # add the unallocated payments to the all payments entry
            for selected_payment in data.selected_payments:
                all_payments_entry.append(selected_payment)

        if len(all_payments_entry) > 0:
            # sort the all payments entry by posting date
            all_payments_entry = sorted(
                all_payments_entry,
                key=lambda k: getdate(str(k.get("posting_date"))),
                reverse=True,
            )
            all_invoices_list = sorted(
                data.selected_invoices,
                key=lambda k: getdate(k.get("posting_date")),
                reverse=True,
            )
            reconcile_doc = frappe.new_doc("Payment Reconciliation")
            reconcile_doc.party_type = "Customer"
            reconcile_doc.party = customer
            reconcile_doc.company = company
            reconcile_doc.receivable_payable_account = get_party_account(
                "Customer", customer, company
            )
            reconcile_doc.get_unreconciled_entries()
            args = {
                "invoices": [],
                "payments": [],
            }
            for invoice in all_invoices_list:
                args["invoices"].append(
                    {
                        "invoice_type": "Sales Invoice",
                        "invoice_number": invoice.get("name"),
                        "invoice_date": invoice.get("posting_date"),
                        "amount": invoice.get("grand_total"),
                        "outstanding_amount": invoice.get("outstanding_amount"),
                        "currency": invoice.get("currency"),
                        "exchange_rate": 0,
                    }
                )
            for payment in all_payments_entry:
                args["payments"].append(
                    {
                        "reference_type": "Payment Entry",
                        "reference_name": payment.get("name"),
                        "posting_date": payment.get("posting_date"),
                        "amount": payment.get("unallocated_amount"),
                        "unallocated_amount": payment.get("unallocated_amount"),
                        "difference_amount": 0,
                        "currency": payment.get("currency"),
                        "exchange_rate": 0,
                    }
                )
            reconcile_doc.allocate_entries(args)
            reconcile_doc.reconcile()

    # then show the results
    msg = ""
    if len(new_payments_entry) > 0:
        msg += "<h4>New Payments</h4>"
        msg += "<table class='table table-bordered'>"
        msg += "<thead><tr><th>Payment Entry</th><th>Amount</th></tr></thead>"
        msg += "<tbody>"
        for payment_entry in new_payments_entry:
            msg += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                payment_entry.get("name"), payment_entry.get("unallocated_amount")
            )
        msg += "</tbody>"
        msg += "</table>"
    if len(all_payments_entry) > 0 and len(data.selected_invoices) > 0:
        msg += "<h4>Reconciled Payments</h4>"
        msg += "<table class='table table-bordered'>"
        msg += "<thead><tr><th>Payment Entry</th><th>Amount</th></tr></thead>"
        msg += "<tbody>"
        for payment_entry in all_payments_entry:
            msg += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                payment_entry.get("name"), payment_entry.get("unallocated_amount")
            )
        msg += "</tbody>"
        msg += "</table>"
    if len(data.selected_invoices) > 0 and data.total_selected_invoices > 0:
        msg += "<h4>Reconciled Invoices</h4>"
        msg += "<table class='table table-bordered'>"
        msg += "<thead><tr><th>Invoice</th><th>Amount</th></tr></thead>"
        msg += "<tbody>"
        for invoice in data.selected_invoices:
            msg += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                invoice.get("name"), invoice.get("outstanding_amount")
            )
        msg += "</tbody>"
        msg += "</table>"
    if len(errors) > 0:
        msg += "<h4>Errors</h4>"
        msg += "<table class='table table-bordered'>"
        msg += "<thead><tr><th>Error</th></tr></thead>"
        msg += "<tbody>"
        for error in errors:
            msg += "<tr><td>{0}</td></tr>".format(error)
        msg += "</tbody>"
        msg += "</table>"
    if len(msg) > 0:
        frappe.msgprint(msg)

    return {
        "new_payments_entry": new_payments_entry,
        "all_payments_entry": all_payments_entry,
        "errors": errors,
        "reconcile_doc": reconcile_doc,
    }


@frappe.whitelist()
def get_available_pos_profiles(company, currency):
    pos_profiles_list = frappe.get_list(
        "POS Profile",
        filters={"disabled": 0, "company": company, "currency": currency},
        page_length=1000,
        pluck="name",
    )
    return pos_profiles_list
