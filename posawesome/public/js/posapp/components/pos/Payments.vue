<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5"
      style="max-height: 80vh; height: 80vh"
    >
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        top
        color="deep-purple accent-4"
      ></v-progress-linear>
      <v-row
        class="pyments px-1 py-0"
        v-for="payment in invoice_doc.payments"
        :key="payment.name"
      >
        <v-col cols="7">
          <v-text-field
            dense
            outlined
            color="indigo"
            :label="payment.mode_of_payment"
            background-color="white"
            hide-details
            v-model="payment.amount"
          ></v-text-field>
        </v-col>
        <v-col cols="5">
          <v-btn block class="" color="success" dark
            >Pay Full {{ payment.mode_of_payment }}</v-btn
          >
        </v-col>
      </v-row>
    </v-card>
    <v-card
      flat
      style="max-height: 10vh; height: 10vh"
      class="cards mb-0 mt-3 py-0"
    >
      <v-row align="start" style="height: 53%">
        <v-col cols="12">
          <v-btn
            block
            class="pa-0"
            large
            color="warning"
            dark
            @click="back_to_invoice"
            >Back</v-btn
          >
        </v-col>
      </v-row>
      <v-row align="end" style="height: 54%">
        <v-col cols="12">
          <v-btn block class="pa-0" large color="success" dark @click="submit">Submit Payments</v-btn>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  data: () => ({
    loading: false,
    invoice_doc: "",
  }),

  methods: {
    back_to_invoice() {
      evntBus.$emit("show_payment", "false");
    },
    submit() {
        this.update_invoice()
        evntBus.$emit("new_invoice", "false");
        this.back_to_invoice()
    },
    update_invoice() {
      frappe.call({
        method: "posawesome.posawesome.api.posapp.update_invoice",
        args: {
          data: this.invoice_doc,
          to_submit: "True"
        },
        async: true,
        callback: function (r) {
          if (r.message) {
            console.log(r.message);
          }
        },
      });
    },
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on("send_invoice_doc_payment", (invoice_doc) => {
        this.invoice_doc = invoice_doc;
        this.invoice_doc.payments[0].amount = invoice_doc.total;
        console.log(invoice_doc.name);
      });
    });
  },

  watch: {},
};
</script>