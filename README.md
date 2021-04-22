## POS AWESOME

### An open-source Point of Sale for [Erpnext](https://github.com/frappe/erpnext) using [Vue.js](https://github.com/vuejs/vue) and [Vuteify](https://github.com/vuetifyjs/vuetify)

---

### Main Features

1. Supports Erpnext Version 12 & 13
2. User friendly and provides a good user experience and speed of use
3. The cashier has the option of either using list view or card view during sales transactions. Card view shows the images of the items
4. Supports invoice submission after printing the receipt for faster printing
5. Supports batch & serial numbering
6. Supports batch based pricing
7. Supports UOM specific barcode and pricing
8. Supports sales of [scale (weighted) products](https://github.com/yrestom/POS-Awesome/discussions/30#discussioncomment-381369)
9. Ability to make returns from POS
10. Supports Making returns for either cash or customer credit
11. Supports using customer credit note for payment
12. Supports credit sales
13. Allows user to choose a due date for credit sales
14. Supports customer loyalty points
15. Shortcuts keys

---

### How to Install

1. `bench get-app https://github.com/yrestom/POS-Awesome.git`
2. `bench setup requirements`
3. `bench build --app posawesome`
4. `bench restart`
5. `bench --site [your.site.name] install-app posawesome`
6. `bench --site [your.site.name] migrate`

---

### Shortcuts:

- `CTRL or CMD + S` open payments
- `CTRL or CMD + X` submit payments
- `CTRL or CMD + D` remove first item from the top
- `CTRL or CMD + A` expand first item from the top
- `CTRL or CMD + E` focus on discount field

---

### Dependencies:

- [Frappe](https://github.com/frappe/frappe)
- [Erpnext](https://github.com/frappe/erpnext)
- [Vue.js](https://github.com/vuejs/vue)
- [Vuetify.js](https://github.com/vuetifyjs/vuetify)

---

### Contributing

Will using for this the same guidelines from Erpnext

1. [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

---

### License

GNU/General Public License (see [license.txt](https://github.com/yrestom/POS-Awesome/blob/master/license.txt))
The POS Awesome code is licensed as GNU General Public License (v3)
