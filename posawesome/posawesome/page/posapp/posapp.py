# -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, add_days
from frappe import _
from erpnext.accounts.party import get_party_account
from posawesome import console


@frappe.whitelist()
def get_items():
	return frappe.db.sql("""
        select *
        from `tabItem`
        order by name
        LIMIT 0, 5000 """
        , as_dict=1)




@frappe.whitelist()
def add_project(pro):
	pro = json.loads(pro)
	doc = frappe.get_doc(dict(
		doctype = "MyProjects",
        title = pro["title"],
        content = pro["content"],
        due = pro["due"],
	)).insert()
	console("data in" , doc)
	return "Project Add"


@frappe.whitelist()
def get_all_projects():
	console("Trigger get_all_projects")
	return frappe.db.sql("""
        select *
        from `tabMyProjects`
        order by name"""
        , as_dict=1)


