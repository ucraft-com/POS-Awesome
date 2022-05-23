# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests
from frappe import _
from requests.auth import HTTPBasicAuth


def get_token(app_key, app_secret, base_url):
    authenticate_uri = "/oauth/v1/generate?grant_type=client_credentials"
    authenticate_url = "{0}{1}".format(base_url, authenticate_uri)

    r = requests.get(authenticate_url, auth=HTTPBasicAuth(app_key, app_secret))

    return r.json()["access_token"]


@frappe.whitelist(allow_guest=True)
def confirmation(**kwargs):
    try:
        args = frappe._dict(kwargs)
        doc = frappe.new_doc("Mpesa Payment Register")
        doc.transactiontype = args.get("TransactionType")
        doc.transid = args.get("TransID")
        doc.transtime = args.get("TransTime")
        doc.transamount = args.get("TransAmount")
        doc.businessshortcode = args.get("BusinessShortCode")
        doc.billrefnumber = args.get("BillRefNumber")
        doc.invoicenumber = args.get("InvoiceNumber")
        doc.orgaccountbalance = args.get("OrgAccountBalance")
        doc.thirdpartytransid = args.get("ThirdPartyTransID")
        doc.msisdn = args.get("MSISDN")
        doc.firstname = args.get("FirstName")
        doc.middlename = args.get("MiddleName")
        doc.lastname = args.get("LastName")
        doc.insert(ignore_permissions=True)
        frappe.log_error("confirmation" + "  " + str(args), "confirmation")
        frappe.db.commit()
        context = {"ResultCode": 0, "ResultDesc": "Accepted"}
        return dict(context)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), str(e))
        context = {"ResultCode": 1, "ResultDesc": "Rejected"}
        return dict(context)


@frappe.whitelist(allow_guest=True)
def validation(**kwargs):
    args = frappe._dict(kwargs)
    frappe.log_error("validation" + "  " + str(args), "validation")
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return dict(context)


@frappe.whitelist()
def get_mpesa_mode_of_payment(company):
    modes = frappe.get_all(
        "Mpesa C2B Register URL",
        filters={"company": company, "register_status": "Success"},
        fields=["mode_of_payment"],
    )
    modes_of_payment = []
    for mode in modes:
        if not mode.mode_of_payment in modes_of_payment:
            modes_of_payment.append(mode.mode_of_payment)
    return modes_of_payment


@frappe.whitelist()
def get_mpesa_draft_payments(company, mode_of_payment, mobile_no=None, full_name=None):
    filters = {"company": company, "mode_of_payment": mode_of_payment, "docstatus": 0}
    if mobile_no:
        filters["msisdn"] = ["like", f"%{mobile_no}%"]
    if full_name:
        filters["full_name"] = ["like", f"%{full_name}%"]

    payments = frappe.get_all(
        "Mpesa Payment Register",
        filters=filters,
        fields=[
            "name",
            "msisdn as mobile_no",
            "full_name",
            "posting_date",
            "transamount as amount",
            "currency",
            "mode_of_payment",
            "company",
        ],
    )
    return payments


@frappe.whitelist()
def submit_mpesa_payment(mpesa_payment, customer):
    doc = frappe.get_doc("Mpesa Payment Register", mpesa_payment)
    doc.customer = customer
    doc.submit_payment = 1
    doc.submit()
    doc.reload()
    return frappe.get_doc("Payment Entry", doc.payment_entry)
