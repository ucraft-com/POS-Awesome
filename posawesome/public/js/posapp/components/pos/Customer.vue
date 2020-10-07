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
        background-color="white"
        no-data-text="Customer not found"
        hide-details
      >
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