## -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import comma_or, nowdate, getdate
from frappe import _
from frappe.model.document import Document

class OverAllowanceError(frappe.ValidationError): pass

def validate_status(status, options):
	if status not in options:
		frappe.throw(_("Status must be one of {0}").format(comma_or(options)))

status_map = {
	"POS Opening Shift": [
		["Draft", None],
		["Open", "eval:self.docstatus == 1 and not self.pos_closing_shift"],
		["Closed", "eval:self.docstatus == 1 and self.pos_closing_shift"],
		["Cancelled", "eval:self.docstatus == 2"],
	]
}

class StatusUpdater(Document):

	def set_status(self, update=False, status=None, update_modified=True):
		if self.is_new():
			if self.get('amended_from'):
				self.status = 'Draft'
			return

		if self.doctype in status_map:
			_status = self.status
			if status and update:
				self.db_set("status", status)

			sl = status_map[self.doctype][:]
			sl.reverse()
			for s in sl:
				if not s[1]:
					self.status = s[0]
					break
				elif s[1].startswith("eval:"):
					if frappe.safe_eval(s[1][5:], None, { "self": self.as_dict(), "getdate": getdate,
							"nowdate": nowdate, "get_value": frappe.db.get_value }):
						self.status = s[0]
						break
				elif getattr(self, s[1])():
					self.status = s[0]
					break

			if self.status != _status and self.status not in ("Cancelled", "Partially Ordered",
																"Ordered", "Issued", "Transferred"):
				self.add_comment("Label", _(self.status))

			if update:
				self.db_set('status', self.status, update_modified = update_modified)
