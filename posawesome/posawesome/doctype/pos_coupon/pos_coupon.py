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
            frappe.throw(
                _("Please select the correct POS Offer with the same company.")
            )
        if not pos_offer.coupon_based:
            frappe.throw(_("Please select Coupon Code Based POS Offer."))
        if pos_offer.disable:
            frappe.throw(_("POS Offer is disable."))
        if pos_offer.valid_from and pos_offer.valid_from > getdate(self.valid_from):
            self.valid_from = pos_offer.valid_from
        if pos_offer.valid_upto and pos_offer.valid_upto < getdate(self.valid_upto):
            self.valid_upto = pos_offer.valid_upto

    def create_coupon_from_referral(self):
        if not self.customer:
            frappe.throw(_("Customer is required"))
        if not self.referral_code:
            frappe.throw(_("Referral Code is required"))
        ref_doc = None
        ref_code_exist = frappe.db.exists("Referral Code", self.referral_code)
        if not ref_code_exist:
            ref_doc = frappe.get_doc(
                "Referral Code", {"referral_code": self.referral_code}
            )
        else:
            ref_doc = frappe.get_doc("Referral Code", self.referral_code)
        if not ref_doc:
            frappe.throw(
                _("Referral Code {0} is not exists").format(self.referral_code)
            )
        if ref_doc.disabled:
            frappe.throw(_("Referral Code {0} is disabled").format(self.referral_code))

        self.coupon_name = frappe.generate_hash()[:10].upper()
        self.coupon_type = "Gift Card"
        self.company = ref_doc.company
        self.pos_offer = ref_doc.customer_offer
        self.campaign = ref_doc.campaign
        self.referral_code = ref_doc.name
        self.save(ignore_permissions=True)

        if ref_doc.primary_offer:
            doc = frappe.new_doc("POS Coupon")
            doc.coupon_name = frappe.generate_hash()[:10].upper()
            doc.coupon_type = "Gift Card"
            doc.company = ref_doc.company
            doc.customer = ref_doc.customer
            doc.pos_offer = ref_doc.primary_offer
            doc.campaign = ref_doc.campaign
            doc.referral_code = ref_doc.name
            doc.save(ignore_permissions=True)


def check_coupon_code(coupon_code, customer=None, company=None):
    res = {"coupon": None}
    if not frappe.db.exists("POS Coupon", {"coupon_code": coupon_code.upper()}):
        res["msg"] = _("Sorry, this coupon code not exists")
        return res

    coupon = frappe.get_doc("POS Coupon", {"coupon_code": coupon_code.upper()})
    pos_offer = frappe.get_doc("POS Offer", coupon.pos_offer)

    if coupon.valid_from:
        if coupon.valid_from > getdate(today()):
            res["msg"] = _("Sorry, this coupon code's validity has not started")
            return res
    if coupon.valid_upto:
        if coupon.valid_upto < getdate(today()):
            res["msg"] = _("Sorry, this coupon code's validity has expired")
            return res
    if coupon.used and coupon.maximum_use and coupon.used >= coupon.maximum_use:
        res["msg"] = _("Sorry, this coupon code is no longer valid")
        return res

    if pos_offer.disable:
        res["msg"] = _("Sorry, this coupon code is no longer valid")
        return res
    if pos_offer.valid_from:
        if pos_offer.valid_from > getdate(today()):
            res["msg"] = _("Sorry, this coupon code's validity has not started")
            return res
    if pos_offer.valid_upto:
        if pos_offer.valid_upto < getdate(today()):
            res["msg"] = _("Sorry, this coupon code's validity has expired")
            return res

    if customer and coupon.coupon_type == "Gift Card":
        if customer != coupon.customer:
            res["msg"] = _("Sorry, this coupon code cannot be used by this customer")
            return res

    if company and coupon.company != company:
        res["msg"] = _("Sorry, this coupon code cannot be used by this company")
        return res

    if customer and coupon.oneـuse:
        count = frappe.db.count(
            "POS Coupon Detail",
            filters={
                "parentfield": "posa_coupons",
                "parenttype": "Sales Invoice",
                "docstatus": 1,
                "customer": customer,
            },
        )
        if count > 0:
            res["msg"] = _("Sorry, {0} have used this coupon before").format(customer)
            return res

    res["coupon"] = coupon
    res["msg"] = "Apply"
    return res


def validate_coupon_code(coupon_code, customer=None, company=None):
    res = check_coupon_code(coupon_code, customer, company)
    if not res.get("coupon"):
        frappe.throw(res.get("msg"))
    else:
        return res


def update_coupon_code_count(coupon_name, transaction_type):
    coupon = frappe.get_doc("POS Coupon", coupon_name)
    if coupon:
        if transaction_type == "used":

            if coupon.maximum_use and coupon.used >= coupon.maximum_use:
                frappe.throw(
                    _("{0} Coupon used are {1}. Allowed quantity is exhausted").format(
                        coupon.coupon_code, coupon.used
                    )
                )
            else:
                coupon.used = coupon.used + 1
                coupon.save(ignore_permissions=True)

        elif transaction_type == "cancelled":
            if coupon.used > 0:
                coupon.used = coupon.used - 1
                coupon.save(ignore_permissions=True)
