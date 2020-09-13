import TableRoot from './CustomerTable.vue';

frappe.provide('frappe.PosApp');




frappe.PosApp.posapp = class {
        constructor({ parent }) {
                this.$parent = $(document);
                this.page = parent.page;
                this.make_body();
                
        }
        make_body() {
                this.$customer_table_container = this.$parent.find('#body_div');
                this.vue = new Vue({
                        vuetify: new Vuetify(),
                        el: this.$customer_table_container[0],
                        data: {
                        },
                        render: h => h(TableRoot),
                });
                
        }       
        setup_header() {
                
        }
};