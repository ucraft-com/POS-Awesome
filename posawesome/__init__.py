# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = "6.0.4"


def console(*data):
    frappe.publish_realtime("toconsole", data, user=frappe.session.user)
