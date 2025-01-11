# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _
from posawesome.posawesome.doctype.referral_code.referral_code import (
    create_referral_code,
)


def after_insert(doc, method):
    create_customer_referral_code(doc)
    create_gift_coupon(doc)


def validate(doc, method):
    validate_referral_code(doc)


def create_customer_referral_code(doc):
    if doc.posa_referral_company:
        company = frappe.get_cached_doc("Company", doc.posa_referral_company)
        if not company.posa_auto_referral:
            return
        create_referral_code(
            doc.posa_referral_company,
            doc.name,
            company.posa_customer_offer,
            company.posa_primary_offer,
            company.posa_referral_campaign,
        )


def create_gift_coupon(doc):
    if doc.posa_referral_code:
        coupon = frappe.new_doc("POS Coupon")
        coupon.customer = doc.name
        coupon.referral_code = doc.posa_referral_code
        coupon.create_coupon_from_referral()


def validate_referral_code(doc):
    referral_code = doc.posa_referral_code
    exist = None
    if referral_code:
        exist = frappe.db.exists("Referral Code", referral_code)
        if not exist:
            exist = frappe.db.exists("Referral Code", {"referral_code": referral_code})
        if not exist:
            frappe.throw(_("This Referral Code {0} not exists").format(referral_code))

@frappe.whitelist()
def get_customer_balance(customer):
    if not customer:
        return {"balance": 0, "customer_name": None}

    try:
        customer_doc = frappe.get_doc("Customer", customer)
        customer_name = customer_doc.customer_name

        # Fetch outstanding balance from GL Entries
        balance = frappe.db.sql("""
            SELECT SUM(debit - credit) AS balance
            FROM `tabGL Entry`
            WHERE party_type = 'Customer' AND party = %s AND docstatus = 1
        """, (customer,), as_dict=True)

        return {
            "balance": flt(balance[0].get("balance", 0)) if balance else 0,
            "customer_name": customer_name
        }
    except Exception as e:
        frappe.log_error(f"Error fetching customer balance: {e}")
        return {"balance": 0, "customer_name": None}