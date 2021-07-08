import Home from './Home.vue';

//import pt from '../../node_modules/vuetify/src/locale/pt'; //HELKYD 08-07-2021
//import { pt } from 'vuetify/src/locale/pt'; //HELKYD 08-07-2021

frappe.provide('frappe.PosApp');


frappe.PosApp.posapp = class {
    constructor({ parent }) {
        this.$parent = $(document);
        this.page = parent.page;
        this.make_body();

    }
    make_body () {
        this.$el = this.$parent.find('.main-section');
        this.vue = new Vue({
            vuetify: new Vuetify(),
            el: this.$el[0],
            data: {
            },
            render: h => h(Home),
        });
    }
    setup_header () {

    }
    
};
/*
export default {
    ...pt,
    invoice: {
        type:{
            title: 'Tipo'
        }
    }
}
*/