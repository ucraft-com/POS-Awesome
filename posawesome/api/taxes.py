# -*- coding: utf-8 -*-
# Copyright (c) 2023, Youssef Restom and contributors
# For license information, please see license.txt


from __future__ import unicode_literals

# import frappe
from frappe.utils import flt
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice


class custom_calculate_taxes_and_totals(calculate_taxes_and_totals):
    def _get_tax_rate(self, tax, item_tax_map):
        if tax.account_head in item_tax_map:
            return flt(item_tax_map.get(tax.account_head), self.doc.precision("rate", tax))
        else:
            return 0


class customSalesInvoice(SalesInvoice):
    def calculate_taxes_and_totals(object):
        return custom_calculate_taxes_and_totals(object)
