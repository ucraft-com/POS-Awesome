# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json


@frappe.whitelist(allow_guest=True)
def confirmation(*args, **kwarg):
    my_str = "args : " + str(args) + " - " + "kwarg : " + str(kwarg)
    frappe.log_error(my_str)


@frappe.whitelist(allow_guest=True)
def validation(*args, **kwarg):
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return dict(context)
