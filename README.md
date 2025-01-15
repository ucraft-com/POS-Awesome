<div align="center">
    <img src="https://frappecloud.com/files/pos.png" height="128">
    <h2>POS AWESOME</h2>
</div>

#### An open-source Point of Sale for [Erpnext](https://github.com/frappe/erpnext) using [Vue.js](https://github.com/vuejs/vue) and [Vuetify](https://github.com/vuetifyjs/vuetify) (VERSION 15 Support)

---

### Main Features

1. Supports Erpnext Version 15
2. User-friendly and provides a good user experience and speed of use
3. The cashier can either use list view or card view during sales transactions. Card view shows the images of the items
4. Supports enqueue invoice submission after printing the receipt for faster processing
5. Supports batch & serial numbering
6. Supports batch-based pricing
7. Supports UOM-specific barcode and pricing
8. Supports sales of scale (weighted) products
9. Ability to make returns from POS
10. Supports Making returns for either cash or customer credit
11. Supports using customer credit notes for payment
12. Supports credit sales
13. Allows the user to choose a due date for credit sales
14. Supports customer loyalty points
15. Shortcut keys
16. Supports Customer Discount
17. Supports POS Offers
18. Auto-apply batches for bundle items
19. Search and add items by Serial Number
20. Create Sales Orders from POS directly
21. Supports template items with variants
22. Supports multiple languages
23. Supports Mpesa mobile payment
24. POS Coupons
25. Supports Referral Code
26. Supports Customer and Customer Group price list
27. Supports Sales Person
28. Supports Delivery Charges
29. Search and add items by Batch Number
30. Accept new payments from customers against existing invoices
31. Payments Reconciliation
32. A lot more bug fixes from the version 14
---

### How to Install

#### ASAERP:

One-click installation is available if you are hosting on [ASAERP](https://asaerp.com) from [here](https://asaerp.com/dashboard/marketplace)

#### Self Hosting:

1. `bench get-app branch version-15 https://github.com/ASATechnologies/POS-Awesome.git`
2. `bench setup requirements`
3. `bench build --app posawesome`
4. `bench restart`
5. `bench --site [your.site.name] install-app posawesome`
6. `bench --site [your.site.name] migrate`

---

### New Features and Bug Report:

- Please Create Github Issue from [here](https://github.com/yrestom/POS-Awesome/issues/new/choose) after checking the existing issues
- For paid features, you can email me [here](mailto:info@totrox.com)

---

### How To Use:

[POS Awesome Wiki](https://github.com/yrestom/POS-Awesome/wiki)

---

### Shortcuts:

- `CTRL or CMD + S` open payments
- `CTRL or CMD + X` submit payments
- `CTRL or CMD + D` remove the first item from the top
- `CTRL or CMD + A` expand the first item from the top
- `CTRL or CMD + E` focus on discount field

---

### Dependencies:

- [Frappe](https://github.com/frappe/frappe)
- [Erpnext](https://github.com/frappe/erpnext)
- [Vue.js](https://github.com/vuejs/vue)
- [Vuetify.js](https://github.com/vuetifyjs/vuetify)

---

### Contributing

1. [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

---

### License

GNU/General Public License (see [license.txt](https://github.com/yrestom/POS-Awesome/blob/master/license.txt))

The POS Awesome code is licensed as GNU General Public License (v3)
