<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
      </template>-->
      <v-card>
        <v-card-title>
          <span class="headline">Create POS Opening Shift</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-autocomplete :items="companys" label="Company" v-model="company" required></v-autocomplete>
              </v-col>
              <v-col cols="12">
                <v-autocomplete
                  :items="pos_profiles"
                  label="POS Profile"
                  v-model="pos_profile"
                  required
                ></v-autocomplete>
              </v-col>
              <v-col cols="12">

                <template>
                  <v-data-table
                    :headers="payments_methods_headers"
                    :items="payments_methods"
                    item-key="mode_of_payment"
                    class="elevation-1"
                    :items-per-page="itemsPerPage"
                    hide-default-footer
                    
                  ></v-data-table>
                </template>

              </v-col>
            </v-row>
          </v-container>
          <small>* indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close_opening_dialog">Close</v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  props: ["dialog"],
  data: () => ({
    dialog_data: {},
    companys: [],
    company: "",
    pos_profiles_data: [],
    pos_profiles: [],
    pos_profile: "",
    payments_method_data : [],
    payments_methods : [],
    payments_methods_headers : [
      {
        text: "Mode of Payment",
        align: "start",
        sortable: false,
        value: "mode_of_payment",
      },
      {
        text: "Opening Amount",
        value: "amount",
        align: "center",
        sortable: false
        },
    ],
    itemsPerPage : 100,
  }),
  watch: {
    company(val) {
      this.pos_profiles = [];
      this.pos_profiles_data.forEach((element) => {
        if (element.company === val) {
          this.pos_profiles.push(element.name);
        }
        if (this.pos_profiles.length) {
          this.pos_profile = this.pos_profiles[0];
        } else {
          this.pos_profile = "";
        }
      });
    },
    pos_profile(val){
        this.payments_methods = []
        this.payments_method_data.forEach((element) => {
        if (element.parent === val) {
          this.payments_methods.push(
              {
                 mode_of_payment: element.mode_of_payment,
                 amount : 0
              }
              );
        }
      });
    },
  },
  methods: {
    close_opening_dialog() {
      evntBus.$emit("close_opening_dialog");
    },
    get_opening_dialog_data() {
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_opening_dialog_data",
        args: {},
        callback: function (r) {
          if (r.message) {
            // r.message.forEach((element) => {
            //   vm.items_group.push(element.name);
            // });
            console.log(r.message);
            r.message.companys.forEach((element) => {
              vm.companys.push(element.name);
            });
            vm.company = vm.companys[0];
            vm.pos_profiles_data = r.message.pos_profiles_data;
            vm.payments_method_data = r.message.payments_method
          }
        },
      });
    },
  },
  created: function () {
    this.$nextTick(function () {
      this.get_opening_dialog_data();
    });
  },
};
</script>
