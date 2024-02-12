// Copyright (c) 2023, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('POSAwesome Settings', {
	onload: function(frm){
		frm.call('get_naming_series_options')
			.then(r => {
				frm.set_df_property("receive_payment_series", "options", r.message);
				frm.set_df_property("pay_payment_series", "options", r.message);
			});
	}
});
