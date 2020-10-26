<template>
  <v-row justify="center">
    <v-dialog v-model="invoicesDialog" max-width="800px" min-width="800px" style="min-height: 500px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">Select Return Invoice</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row class="mb-4">
              <v-text-field
            color="indigo"
            label="Invoice ID"
            background-color="white"
            hide-details
            v-model="invoice_name"
            dense
          ></v-text-field>
          <v-btn class="ml-4" color="primary" dark @click="search_invoices">Search</v-btn>
            </v-row>
            <v-row>
              <v-col cols="12" class="pa-1"  v-if="dialog_data">
                <template>
                  <v-data-table
                    :headers="headers"
                    :items="dialog_data"
                    item-key="name"
                    class="elevation-1"
                    :single-select="singleSelect"
                    show-select
                    v-model="selected"
                  >
                  </v-data-table>
                </template>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="mt-4">
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
          <v-btn v-if="selected.length" color="primary" dark @click="submit_dialog">Select</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  data: () => ({
    invoicesDialog: false,
    singleSelect: true,
    selected: [],
    dialog_data: "",
    company: "",
    invoice_name:"",
    headers: [
      {
        text: "Customer",
        value: "customer",
        align: "start",
        sortable: true,
      },
      {
        text: "Date",
        align: "start",
        sortable: true,
        value: "posting_date",
      },
      {
        text: "Invoice",
        value: "name",
        align: "start",
        sortable: true,
      },
      {
        text: "Amount",
        value: "grand_total",
        align: "start",
        sortable: false,
      },
    ],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.invoicesDialog = false;
    },
    search_invoices() {
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.search_invoices",
        args: {
          invoice_name: vm.invoice_name,
          company: vm.company,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            // evntBus.$emit("open_drafts", r.message);
            vm.dialog_data = r.message;
          }
        },
      });
    },
    submit_dialog() {
      if (this.selected.length > 0) {
        this.selected[0].is_returnm = 1;
        evntBus.$emit("load_invoice", this.selected[0]);
        this.invoicesDialog = false;
      }
    },
  },
  created: function () {
    evntBus.$on("open_returns", (data) => {
      this.invoicesDialog = true;
      this.company = data;
      this.invoice_name = "";
      this.dialog_data = "";
    });
  },
};
</script>
