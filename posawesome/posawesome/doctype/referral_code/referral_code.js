// Copyright (c) 2021, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Referral Code', {
	setup: function (frm) {
		frm.set_query("party_type", function () {
			return {
				filters: {
					"name": ["in", ["Customer"]],
				}
			};
		});
		frm.set_query("customer_offer", function () {
			return {
				filters: {
					"company": frm.doc.company,
					"coupon_based": 1,
					"disable": 0,
				}
			};
		});
		frm.set_query("primary_offer", function () {
			return {
				filters: {
					"company": frm.doc.company,
					"coupon_based": 1,
					"disable": 0,
				}
			};
		});
	},
	referral_name: function (frm) {
		if (frm.doc.__islocal === 1) {
			frm.trigger("make_referral_code");
		}
	},
	make_referral_code: function (frm) {
		let referral_name = frm.doc.referral_name;
		let referral_code;
		if (!referral_name) {
			frm.doc.referral_name = frm.doc.party + Math.random().toString(5).substring(2, 5).toUpperCase();
			referral_code = Math.random().toString(12).substring(2, 12).toUpperCase();
		}
		else {
			referral_name = referral_name.replace(/\s/g, '');
			referral_code = referral_name.toUpperCase().slice(0, 8);
		}
		frm.doc.referral_code = referral_code;
		frm.refresh_field('referral_name');
		frm.refresh_field('referral_code');
	},

});
