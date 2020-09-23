# -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, add_days
from frappe import _
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability
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
def get_items(pos_profile):
    
    pos_profile = json.loads(pos_profile)
    warehouse = pos_profile.get("warehouse")
    price_list = pos_profile.get("selling_price_list")

    item_groups_list = []
    if pos_profile.get("item_groups"):
        for group in pos_profile.get("item_groups"):
            if not frappe.db.exists('Item Group', group.get("item_group")):
                item_group = get_root_of(group.get("item_group"))
                item_groups_list.append(item_group)
            else:
                item_groups_list.append(group.get("item_group"))

    conditon = ""
    if len(item_groups_list) > 0:
        if len(item_groups_list) == 1:
            conditon = "AND item_group = '{0}'".format(item_groups_list[0])
        else:
            conditon = "AND item_group in {0}".format(tuple(item_groups_list))


    result = []

    items_data = frappe.db.sql("""
        SELECT
            name AS item_code,
            item_name,
            description,
            stock_uom,
            image,
            idx AS idx,
            is_stock_item,
            has_variants,
            item_group
        FROM
            `tabItem`
        WHERE
            disabled = 0
                AND is_sales_item = 1
                AND is_fixed_asset = 0
                {0}
        ORDER BY
            name asc
            """
        .format(
            conditon
        ), as_dict=1)

    if items_data:
        items = [d.item_code for d in items_data]
        item_prices_data = frappe.get_all("Item Price",
            fields = ["item_code", "price_list_rate", "currency"],
            filters = {'price_list': price_list, 'item_code': ['in', items]})

        item_prices = {}
        for d in item_prices_data:
            item_prices[d.item_code] = d

        for item in items_data:
            item_code = item.item_code
            item_price = item_prices.get(item_code) or {}
            item_stock_qty = get_stock_availability(item_code, warehouse)

            # if not item_stock_qty:
            #     pass
            # else:
            row = {}
            row.update(item)
            row.update({
                'price_list_rate': item_price.get('price_list_rate') or 0,
                'currency': item_price.get('currency') or pos_profile.get("currency"),
                'actual_qty': item_stock_qty or 0,
            })
            result.append(row)


    return result


def get_root_of(doctype):
	"""Get root element of a DocType with a tree structure"""
	result = frappe.db.sql("""select t1.name from `tab{0}` t1 where
		(select count(*) from `tab{1}` t2 where
			t2.lft < t1.lft and t2.rgt > t1.rgt) = 0
		and t1.rgt > t1.lft""".format(doctype, doctype))
	return result[0][0] if result else None

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
