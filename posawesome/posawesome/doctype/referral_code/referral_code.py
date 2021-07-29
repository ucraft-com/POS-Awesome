# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import strip


class ReferralCode(Document):
    def autoname(self):
        if not self.referral_name:
            self.referral_name = (
                strip(self.party) + "-" + frappe.generate_hash()[:5].upper()
            )
            self.name = self.referral_name
        else:
            self.referral_name = strip(self.referral_name)
            self.name = self.referral_name

        if not self.referral_code:
            self.referral_code = frappe.generate_hash()[:10].upper()


@frappe.whitelist()
def get_party_details(party_type, party):

    if not frappe.db.exists(party_type, party):
        frappe.throw(_("Invalid {0}: {1}").format(party_type, party))

    _party_name = (
        "title"
        if party_type in ("Student", "Sales Partner")
        else party_type.lower() + "_name"
    )
    party_name = frappe.db.get_value(party_type, party, _party_name)

    return party_name
