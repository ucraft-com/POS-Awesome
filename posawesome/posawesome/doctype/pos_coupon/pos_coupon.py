# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import strip
from frappe.utils import getdate, today


class POSCoupon(Document):
    def autoname(self):
        self.coupon_name = strip(self.coupon_name)
        self.name = self.coupon_name

        if not self.coupon_code:
            if self.coupon_type == "Promotional":
                self.coupon_code = "".join(
                    i for i in self.coupon_name if not i.isdigit()
                )[0:8].upper()
            elif self.coupon_type == "Gift Card":
                self.coupon_code = frappe.generate_hash()[:10].upper()

    def validate(self):
        if self.coupon_type == "Gift Card":
            self.maximum_use = 1
            if not self.customer:
                frappe.throw(_("Please select the customer."))
        pos_offer = frappe.get_doc("POS Offer", self.pos_offer)
        if self.company != pos_offer.company:
            frappe.throw(_("Please select correct POS Offer with the same company."))
        if not pos_offer.coupon:
            frappe.throw(_("Please select Coupon Code Based POS Offer."))
        if pos_offer.disable:
            frappe.throw(_("POS Offer is disable."))
        if pos_offer.valid_from and pos_offer.valid_from > self.valid_from:
            self.valid_from = pos_offer.valid_from
        if pos_offer.valid_upto and pos_offer.valid_upto < self.valid_upto:
            self.valid_upto = pos_offer.valid_upto


def validate_coupon_code(coupon_name):
    coupon = frappe.get_doc("POS Coupon", coupon_name)
    pos_offer = frappe.get_doc("POS Offer", coupon.pos_offer)

    if coupon.valid_from:
        if coupon.valid_from > getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has not started"))
    elif coupon.valid_upto:
        if coupon.valid_upto < getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has expired"))
    elif coupon.used >= coupon.maximum_use:
        frappe.throw(_("Sorry, this coupon code is no longer valid"))

    if pos_offer.disable:
        frappe.throw(_("Sorry, this coupon code is no longer valid."))
    elif pos_offer.valid_from:
        if pos_offer.valid_from > getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has not started"))
    elif pos_offer.valid_upto:
        if pos_offer.valid_upto < getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has expired"))


def update_coupon_code_count(coupon_name, transaction_type):
    coupon = frappe.get_doc("POS Coupon", coupon_name)
    if coupon:
        if transaction_type == "used":
            if coupon.used < coupon.maximum_use:
                coupon.used = coupon.used + 1
                coupon.save(ignore_permissions=True)
            else:
                frappe.throw(
                    _("{0} Coupon used are {1}. Allowed quantity is exhausted").format(
                        coupon.coupon_code, coupon.used
                    )
                )
        elif transaction_type == "cancelled":
            if coupon.used > 0:
                coupon.used = coupon.used - 1
                coupon.save(ignore_permissions=True)
