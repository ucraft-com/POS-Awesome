<template>
  <div>
    <v-autocomplete density="compact" clearable auto-select-first variant="outlined" color="primary"
      :label="frappe._('Customer')" v-model="customer" :items="customers" item-title="customer_name" item-value="name"
      bg-color="white" :no-data-text="__('Customer not found')" hide-details :customFilter="customFilter"
      :disabled="readonly" append-icon="mdi-plus" @click:append="new_customer" prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer">
      <template v-slot:default="data">
        <template>

          <v-list-item-title class="text-primary text-subtitle-1">
            <div v-html="data.item.customer_name"></div>
          </v-list-item-title>
          <v-list-item-subtitle v-if="data.item.customer_name != data.item.name">
            <div v-html="`ID: ${data.item.name}`"></div>
          </v-list-item-subtitle>
          <v-list-item-subtitle v-if="data.item.tax_id">
            <div v-html="`TAX ID: ${data.item.tax_id}`"></div>
          </v-list-item-subtitle>
          <v-list-item-subtitle v-if="data.item.email_id">
            <div v-html="`Email: ${data.item.email_id}`"></div>
          </v-list-item-subtitle>
          <v-list-item-subtitle v-if="data.item.mobile_no">
            <div v-html="`Mobile No: ${data.item.mobile_no}`"></div>
          </v-list-item-subtitle>
          <v-list-item-subtitle v-if="data.item.primary_address">
            <div v-html="`Primary Address: ${data.item.primary_address}`"></div>
          </v-list-item-subtitle>


        </template>
      </template>
    </v-autocomplete>
    <div class="mb-8">
      <UpdateCustomer></UpdateCustomer>
    </div>
  </div>
</template>

<script>

import UpdateCustomer from './UpdateCustomer.vue';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    customer_info: {},
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    get_customer_names() {
      var vm = this;
      if (this.customers.length > 0) {
        return;
      }
      if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }

      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {

            vm.customers = r.message;

            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }

          }
        },
      });
    },
    new_customer() {
      this.eventBus.emit('open_update_customer', null);
    },
    edit_customer() {
      this.eventBus.emit('open_update_customer', this.customer_info);
    },
    customFilter(itemText, queryText, itemRow) {
      const item = itemRow.raw;
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      this.eventBus.on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      this.eventBus.on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      this.eventBus.on('set_customer', (customer) => {
        this.customer = customer;
      });
      this.eventBus.on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      this.eventBus.on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      this.eventBus.on('set_customer_info_to_edit', (data) => {
        this.customer_info = data;
      });
      this.eventBus.on('fetch_customer_details', () => {
        this.get_customer_names();
      });
    });
  },

  watch: {
    customer() {
      this.eventBus.emit('update_customer', this.customer);
    },
  },
};
</script>
