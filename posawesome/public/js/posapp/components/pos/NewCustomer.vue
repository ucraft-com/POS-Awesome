<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
      </template>-->
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">New Customer</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="indigo"
                  label="Customer Name"
                  background-color="white"
                  hide-details
                  v-model="customer_name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  label="Tax ID"
                  background-color="white"
                  hide-details
                  v-model="tax_id"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  label="Mobile No"
                  background-color="white"
                  hide-details
                  v-model="mobile_no"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  label="Email Id"
                  background-color="white"
                  hide-details
                  v-model="email_id"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
          <v-btn color="primary" dark @click="submit_dialog">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  // props: ["draftsDialog"],
  data: () => ({
    customerDialog: false,
    customer_name: "",
    tax_id: "",
    mobile_no: "",
    email_id: "",
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.customerDialog = false;
    },

    submit_dialog() {
      if (this.customer_name) {
        const vm = this;
        const args = {
            customer_name: this.customer_name,
            tax_id: this.tax_id,
            mobile_no: this.mobile_no,
            email_id: this.email_id,
        };
        frappe.call({
          method: "posawesome.posawesome.api.posapp.create_customer",
          args: args,
          callback: (r) => {
            if (!r.exc && r.message.name) {
              evntBus.$emit("show_mesage", {
                text: "Customer contact created successfully.",
                color: "success",
              });
              args.name = r.message.name
              frappe.utils.play_sound("submit");
              evntBus.$emit("add_customer_to_list", args);
              evntBus.$emit("set_customer", r.message.name);
              this.customer_name = "";
              this.tax_id = "";
              this.mobile_no = "";
              this.email_id = "";
            }
          },
        });
        this.customerDialog = false;
      }
    },
  },
  created: function () {
    evntBus.$on("open_new_customer", () => {
      this.customerDialog = true;
    });
  },
};
</script>
