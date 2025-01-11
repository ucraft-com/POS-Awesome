// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['POS Opening Shift'] = {
	get_indicator: function(doc) {
		var status_color = {
			"Draft": "grey",
			"Open": "orange",
			"Closed": "green",
			"Cancelled": "red"

		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	}
};
