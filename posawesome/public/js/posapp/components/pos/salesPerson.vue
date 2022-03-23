<template>
  <div>
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="indigo"
      :label="frappe._('Sales Person')"
      v-model="sales_person"
      :items="sales_person_name"
      :value="name"
      item-text="sales_person_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Sales Person not found')"
      hide-details
      v-on:change='onChange'
      :disabled="readonly"
      prepend-inner-icon="mdi-account-edit"
    ></v-autocomplete>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    sales_person: null,
    sales_person_name: [],
    sales_team: [
      {
        "sales_person":"",
        "allocated_percentage":100,
        "parentfield":"sales_team",
        "parenttype":"Sales Invoice",
        "doctype": "Sales Team"
      }
    ],
  }),

  methods: {
    get_sales_person_names() {
      const vm = this;
  
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_sales_person',
        args: {},
        callback: function (r) {
          if (r.message) {
            vm.sales_person_name = Object.keys(r.message);
            console.info('loadSalesPerson');
          }
        },
      });
    },

    onChange: function (e){
      if(e != undefined){
        this.sales_team[0]['sales_person'] = e;
        evntBus.$emit('set_sales_team', this.sales_team);
      }else{
        evntBus.$emit('set_sales_team', []);
      }
    }
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.get_sales_person_names();
      });
    });
    evntBus.$on('reset_sales_team', () => {
      this.sales_person = null;
      evntBus.$emit('set_sales_team', []);
    });
  },
};
</script>