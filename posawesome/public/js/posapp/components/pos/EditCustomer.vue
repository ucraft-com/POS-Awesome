<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{ __('Customer Info') }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Customer Name')"
                  background-color="white"
                  hide-details
                  readonly
                  v-model="customer_info.name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Email')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.email_id"
                  @change="set_customer_info('email_id', $event)"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Mobile No')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.mobile_no"
                  @change="set_customer_info('mobile_no', $event)"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="customer_info.loyalty_program"
                  :label="frappe._('Loyalty Program')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="customer_info.loyalty_points"
                  :label="frappe._('Loyalty Points')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    customerDialog: false,
    customer_info: '',
  }),

  watch: {
    customer() {
      this.fetch_customer_details();
    },
  },

  methods: {
    close_dialog() {
      this.customerDialog = false;
    },

    set_customer_info(field, value) {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.set_customer_info',
        args: {
          fieldname: field,
          customer: this.customer_info.name,
          value: value,
        },
        callback: (r) => {
          if (!r.exc) {
            vm.customer_info[field] = value;
            evntBus.$emit('show_mesage', {
              text: __('Customer contact updated successfully.'),
              color: 'success',
            });
            frappe.utils.play_sound('submit');
          }
        },
      });
    },
  },
  created: function () {
    evntBus.$on('open_edit_customer', () => {
      this.customerDialog = true;
    });
    evntBus.$on('set_customer_info_to_edit', (data) => {
      this.customer_info = data;
    });
  },
};
</script>
