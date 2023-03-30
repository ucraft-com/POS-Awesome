// Copyright (c) 2023, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Day Close Setting', {
	refresh: function(frm) {
		frm.fields_dict["profile_list"].grid.add_custom_button(__('Get Profiles'), 
			function() {
				frappe.db.get_list('POS Profile', {	fields: ['name'],}).then(records => {
					// frappe.msgprint(records)
					frm.doc.profile_list = []
					for(let row of records){
						// console.log(row.name)
						frm.add_child('profile_list', {
							profile: row.name,
							
						});
						frm.refresh_field('profile_list');
						
					}
				})
				
        });
	}
});
