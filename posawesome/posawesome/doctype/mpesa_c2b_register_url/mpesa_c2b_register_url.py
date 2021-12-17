# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe, requests
from frappe.model.document import Document
from frappe.utils import get_request_site_address
from posawesome.posawesome.api.m_pesa import get_token


class MpesaC2BRegisterURL(Document):
    def validate(self):
        sandbox_url = "https://sandbox.safaricom.co.ke"
        live_url = "https://api.safaricom.co.ke"
        mpesa_settings = frappe.get_doc("Mpesa Settings", self.mpesa_settings)
        env = "production" if not mpesa_settings.sandbox else "sandbox"
        business_shortcode = (
            mpesa_settings.business_shortcode
            if env == "production"
            else mpesa_settings.till_number
        )
        if env == "sandbox":
            base_url = sandbox_url
        else:
            base_url = live_url
        token = get_token(
            app_key=mpesa_settings.consumer_key,
            app_secret=mpesa_settings.get_password("consumer_secret"),
            base_url=base_url,
        )
        site_url = get_request_site_address(True)
        validation_url = (
            site_url + "/api/method/posawesome.posawesome.api.m_pesa.validation"
        )
        confirmation_url = (
            site_url + "/api/method/posawesome.posawesome.api.m_pesa.confirmation"
        )
        register_url = base_url + "/mpesa/c2b/v1/registerurl"

        payload = {
            "ShortCode": business_shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": validation_url,
            "ValidationURL": confirmation_url,
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
