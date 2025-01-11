# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from posawesome.posawesome.api.payment_entry import create_payment_entry


class MpesaPaymentRegister(Document):
    def before_insert(self):
        self.set_missing_values()

    def set_missing_values(self):
        self.currency = "KES"
        self.full_name = ""
        if self.firstname:
            self.full_name = self.firstname
        if self.middlename:
            self.full_name += " " + self.middlename
        if self.lastname:
            self.full_name += " " + self.lastname

        register_url_list = frappe.get_all(
            "Mpesa C2B Register URL",
            filters={
                "business_shortcode": self.businessshortcode,
                "register_status": "Success",
            },
            fields=["company", "mode_of_payment"],
        )
        if len(register_url_list) > 0:
            self.company = register_url_list[0].company
            self.mode_of_payment = register_url_list[0].mode_of_payment

    def before_submit(self):
        if not self.transamount:
            frappe.throw(_("Trans Amount is required"))
        if not self.company:
            frappe.throw(_("Company is required"))
        if not self.customer:
            frappe.throw(_("Customer is required"))
        if not self.mode_of_payment:
            frappe.throw(_("Mode of Payment is required"))
        self.payment_entry = self.create_payment_entry()

    def create_payment_entry(self):
        payment_entry = create_payment_entry(
            self.company,
            self.customer,
            self.transamount,
            self.currency,
            self.mode_of_payment,
            self.posting_date,
            self.transid,
            self.posting_date,
            None,
            self.submit_payment,
        )
        return payment_entry.name
