# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document
from frappe.utils import get_request_site_address
from posawesome.posawesome.api.m_pesa import get_token


class MpesaC2BRegisterURL(Document):
    def validate(self):
        sandbox_url = "https://sandbox.safaricom.co.ke"
        live_url = "https://api.safaricom.co.ke"
        env = "production" if not self.sandbox else "sandbox"
        business_shortcode = self.business_shortcode

        if env == "sandbox":
            base_url = sandbox_url
        else:
            base_url = live_url
        token = get_token(
            app_key=self.consumer_key,
            app_secret=self.get_password("consumer_secret"),
            base_url=base_url,
        )
        site_url = get_request_site_address(True)
        confirmation_url = (
            site_url + "/api/method/posawesome.posawesome.api.m_pesa.confirmation"
        )
        validation_url = (
            site_url + "/api/method/posawesome.posawesome.api.m_pesa.validation"
        )
        register_url = base_url + "/mpesa/c2b/v2/registerurl"

        payload = {
            "ShortCode": business_shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(token),
            "Content-Type": "application/json",
        }
        r = requests.post(register_url, headers=headers, json=payload)
        res = r.json()
        if res.get("ResponseDescription") == "Success":
            self.register_status = "Success"
        else:
            self.register_status = "Failed"
            frappe.msgprint(str(res))