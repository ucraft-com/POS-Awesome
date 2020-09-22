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
        v-model="cutomer"
        :items="cutomers"
        append-outer-icon="mdi-plus"
        background-color="white"
        no-data-text="Customer not found"
        hide-details
      ></v-autocomplete>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    cutomers: ["Cash Customer", "foo", "bar", "fizz", "buzz"],
    cutomer: "",
  }),

  methods: {
    get_customer_names() {
      const vm = this;
      if (localStorage.customer_storage) {
        vm.cutomers = JSON.parse(localStorage.getItem("customer_storage"));
      }
      
      frappe.call({
        method: "posawesome.posawesome.page.posapp.posapp.get_customer_names",
        args: {},
        callback: function (r) {
          if (r.message) {
            const loadCustomers =
              !localStorage.customer_storage ||
              JSON.parse(localStorage.getItem("items_storage")).length !=
                r.message.length;
            localStorage.setItem("customer_storage", "");
            localStorage.setItem("customer_storage", JSON.stringify(r.message));
            if (loadCustomers) {
              vm.$nextTick(() => {
                console.log("loadCustomers", loadCustomers);
                vm.cutomers = JSON.parse(
                  localStorage.getItem("customer_storage")
                );
              });
            }
          }
        },
      });
    },
  },
  computed: {},

  created: function () {
    this.$nextTick(function () {
      this.get_customer_names();
    });
  },
};
</script>