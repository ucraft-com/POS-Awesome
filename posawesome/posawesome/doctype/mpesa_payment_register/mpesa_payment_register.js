// Copyright (c) 2021, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mpesa Payment Register", {
	refresh: function (frm) {
		if (frm.doc.docstatus == 1) {
			if (frm.doc.transamount > 0) {
				frm.add_custom_button(__("Create Payment Entry"), function () {
					frm.trigger("make_payment_entry");
				});
			}
		}
	},

	make_payment_entry: function (frm) {
		let fields = [{
			"fieldtype": "Link",
			"label": __("Mode of Payment"),
			"fieldname": "mode_of_payment",
			"options": "Mode of Payment",
			"default": frm.doc.mode_of_payment
		}];

		if (!frm.doc.customer) {
			fields.push({
				"fieldtype": "Link",
				"label": __("Customer"),
				"fieldname": "customer",
				"options": "Customer",
				"default": frm.doc.customer,
				"reqd": 1,
			});
		}

		let dialog = new frappe.ui.Dialog({
			title: __("Create Payment Entry"),
			fields: fields
		});

		dialog.set_primary_action(__('Create Payment Entry'), () => {
			var args = dialog.get_values();
			if (!args) return;
			dialog.hide();
			return frappe.call({
				type: "GET",
				method: "posawesome.posawesome.doctype.mpesa_payment_register.mpesa_payment_register.create_payment_entry", args: {
					"mode_of_payment": frm.doc.mode_of_payment || args.mode_of_payment,
					"customer": frm.doc.customer || args.customer,
					"currency": frm.doc.currency
				},
				freeze: true,
				callback: function (r) {
					if (!r.exc && r.message) {
						frm.set_value("mode_of_payment", r.message.name);
						frappe.model.sync(r.message);
						frappe.set_route("Form", r.message.doctype, r.message.name);
					}
				}
			});
		});
		dialog.show();
	}
});