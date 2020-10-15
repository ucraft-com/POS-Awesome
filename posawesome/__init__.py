# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
__version__ = '0.0.6'

def console(*data):
	frappe.publish_realtime('toconsole', data, user=frappe.session.user)