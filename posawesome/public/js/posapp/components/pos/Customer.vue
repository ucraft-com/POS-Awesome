<template>
  <v-row class="items px-2 py-1">
    <v-col cols="12" class="pb-0 mb-2">
      <v-autocomplete
        dense
        clearable
        autofocus
        auto-select-first
        outlined
        color="indigo"
        label="Customer"
        v-model="customer"
        :items="customers"
        item-text="name"
        background-color="white"
        no-data-text="Customer not found"
        hide-details
        :filter="customFilter"
      >
        <template v-slot:item="data">
          <template>
            <v-list-item-content>
              <v-list-item-title class="indigo--text subtitle-1"
                v-html="data.item.name"
              ></v-list-item-title>
              <v-list-item-subtitle v-if="data.item.tax_id"
                v-html="
                  `TAX ID: ${data.item.tax_id}`
                "
              ></v-list-item-subtitle>
              <v-list-item-subtitle v-if="data.item.email_id"
                v-html="
                  `Email: ${data.item.email_id}`
                "
              ></v-list-item-subtitle>
              <v-list-item-subtitle v-if="data.item.mobile_no"
                v-html="
                  `Mobile No: ${data.item.mobile_no}`
                "
              ></v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </template>
        <template v-slot:append-outer>
          <v-slide-x-reverse-transition mode="out-in">
            <v-icon @click="new_customer">mdi-plus</v-icon>
          </v-slide-x-reverse-transition>
        </template>
      </v-autocomplete>
    </v-col>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  data: () => ({
    pos_profile: "",
    customers: [],
    customer: "",
  }),

  methods: {
    get_customer_names() {
      const vm = this;
      if (localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem("customer_storage"));
      }

      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_customer_names",
        args: {},
        callback: function (r) {
          if (r.message) {
            localStorage.setItem("customer_storage", "");
            localStorage.setItem("customer_storage", JSON.stringify(r.message));
            vm.$nextTick(() => {
              console.log("loadCustomers");
              vm.customers = JSON.parse(
                localStorage.getItem("customer_storage")
              );
            });
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit("open_new_customer");
    },
    customFilter (item, queryText, itemText) {
        const textOne = item.name.toLowerCase()
        const textTwo = item.tax_id ? item.tax_id.toLowerCase() : ""
        const textThree = item.email_id ? item.email_id.toLowerCase() : ""
        const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : ""
        const searchText = queryText.toLowerCase()

        return textOne.indexOf(searchText) > -1 ||
          textTwo.indexOf(searchText) > -1 || 
          textThree.indexOf(searchText) > -1 || 
          textFour.indexOf(searchText) > -1

      },
  },
  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on("register_pos_profile", (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on("set_customer", (customer) => {
        this.customer = customer;
      });
      evntBus.$on("add_customer_to_list", (customer) => {
        this.customers.push(customer);
      });
    });
  },

  watch: {
    customer() {
      evntBus.$emit("update_customer", this.customer);
    },
  },
};
</script>