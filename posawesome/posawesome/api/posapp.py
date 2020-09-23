# -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, add_days
from frappe import _
from erpnext.accounts.party import get_party_account
import json
from posawesome import console


@frappe.whitelist()
def get_opening_dialog_data():
    data = {}
    data["companys"] = frappe.get_list(
        "Company", limit_page_length=0, order_by='name')
    data["pos_profiles_data"] = frappe.get_list(
        "POS Profile", fields=["name", "company"], limit_page_length=0, order_by='name')

    pos_profiles_list = []
    for i in data["pos_profiles_data"]:
        pos_profiles_list.append(i.name)

    data["payments_method"] = frappe.get_list(
        "POS Payment Method",
        filters={"parent": ["in", pos_profiles_list]},
        fields=["*"],
        limit_page_length=0,
        order_by='parent'
    )

    return data


@frappe.whitelist()
def create_opening_voucher(pos_profile, company, balance_details):
    import json
    balance_details = json.loads(balance_details)

    new_pos_opening = frappe.get_doc({
        'doctype': 'POS Opening Shift',
        "period_start_date": frappe.utils.get_datetime(),
        "posting_date": frappe.utils.getdate(),
        "user": frappe.session.user,
        "pos_profile": pos_profile,
        "company": company,
    })
    new_pos_opening.set("balance_details", balance_details)
    new_pos_opening.submit()
    data = {}
    data["pos_opening_shift"] = new_pos_opening.as_dict()
    data["pos_profile"] = frappe.get_doc(
        "POS Profile", new_pos_opening.pos_profile)
    return data


@frappe.whitelist()
def check_opening_shift(user):
    open_vouchers = frappe.db.get_all("POS Opening Shift",
                                      filters={
                                          "user": user,
                                          "pos_closing_entry": ["in", ["", None]],
                                          "docstatus": 1
                                      },
                                      fields=["name",
                                              "pos_profile"],
                                      order_by="period_start_date desc"
                                      )
    data = ""
    if len(open_vouchers) > 0:
        data = {}
        data["pos_opening_shift"] = frappe.get_doc(
            "POS Opening Shift", open_vouchers[0]["name"])
        data["pos_profile"] = frappe.get_doc(
            "POS Profile", open_vouchers[0]["pos_profile"])
    return data


@frappe.whitelist()
def get_items():
    return frappe.db.sql("""
        select name ,item_code, item_name, image, item_group, stock_uom
        from `tabItem`
        order by name
        LIMIT 0, 10000 """, as_dict=1)


@frappe.whitelist()
def get_items_groups():
    return frappe.db.sql("""
        select name 
        from `tabItem Group`
        where is_group = 0
        order by name
        LIMIT 0, 200 """, as_dict=1)


@frappe.whitelist()
def get_customer_names():
    customers = frappe.db.sql("""
        select name 
        from `tabCustomer`
        order by name
        LIMIT 0, 10000 """, as_dict=1)
    customers_list = []
    for customer in customers:
        customers_list.append(customer["name"])
    return customers_list


# @frappe.whitelist()
# def add_project(pro):
# 	pro = json.loads(pro)
# 	doc = frappe.get_doc(dict(
# 		doctype = "MyProjects",
#         title = pro["title"],
#         content = pro["content"],
#         due = pro["due"],
# 	)).insert()
# 	console("data in" , doc)
# 	return "Project Add"


# @frappe.whitelist()
# def get_all_projects():
# 	console("Trigger get_all_projects")
# 	return frappe.db.sql("""
#         select *
#         from `tabMyProjects`
#         order by name"""
#         , as_dict=1)
