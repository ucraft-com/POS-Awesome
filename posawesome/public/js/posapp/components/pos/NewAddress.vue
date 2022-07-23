<template>
  <v-row justify="center">
    <v-dialog v-model="addressDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{
            __('Add New Address')
          }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Address Name')"
                  background-color="white"
                  hide-details
                  v-model="address.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Address Line 1')"
                  background-color="white"
                  hide-details
                  v-model="address.address_line1"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Address Line 2')"
                  background-color="white"
                  hide-details
                  v-model="address.address_line2"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="City"
                  dense
                  color="primary"
                  background-color="white"
                  hide-details
                  v-model="address.city"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="State"
                  dense
                  background-color="white"
                  hide-details
                  v-model="address.state"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="success" dark @click="submit_dialog">{{
            __('Submit')
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    addressDialog: false,
    address: {},
    customer: '',
  }),

  methods: {
    close_dialog() {
      this.addressDialog = false;
    },

    submit_dialog() {
      const vm = this;
      this.address.customer = this.customer;
      this.address.doctype = 'Customer';
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.make_address',
        args: {
          args: this.address,
        },
        callback: (r) => {
          if (!r.exc) {
            evntBus.$emit('add_the_new_address', r.message);
            evntBus.$emit('show_mesage', {
              text: 'Customer Address created successfully.',
              color: 'success',
            });
            vm.addressDialog = false;
            vm.customer = '';
            vm.address = {};
          }
        },
      });
    },
  },
  created: function () {
    evntBus.$on('open_new_address', (data) => {
      this.addressDialog = true;
      this.customer = data;
    });
  },
};
</script>
