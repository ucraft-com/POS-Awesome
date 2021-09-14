// Copyright (c) 2021, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Company', {
    setup: function (frm) {
        frm.set_query("posa_customer_offer", function () {
            return {
                filters: {
                    "company": frm.doc.name,
                    "coupon_based": 1,
                    "disable": 0,
                }
            };
        });
        frm.set_query("posa_primary_offer", function () {
            return {
                filters: {
                    "company": frm.doc.name,
                    "coupon_based": 1,
                    "disable": 0,
                }
            };
        });
    },
});