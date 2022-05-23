<template>
  <v-row justify="center">
    <v-dialog v-model="draftsDialog" max-width="800px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
      </template>-->
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{__('Select Hold Invoice')}}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12" class="pa-1">
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
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
          <v-btn color="primary" dark @click="submit_dialog">Select</v-btn>
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
    draftsDialog: false,
    singleSelect: true,
    selected: [],
    dialog_data: {},
    headers: [
      {
        text: __("Customer"),
        value: "customer",
        align: "start",
        sortable: true,
      },
      {
        text: __("Date"),
        align: "start",
        sortable: true,
        value: "posting_date",
      },
      {
        text: __("Invoice"),
        value: "name",
        align: "start",
        sortable: true,
      },
      {
        text: __("Amount"),
        value: "grand_total",
        align: "start",
        sortable: false,
      },
    ],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.draftsDialog = false;
    },

    submit_dialog() {
      if (this.selected.length > 0) {
        evntBus.$emit("load_invoice", this.selected[0]);
        this.draftsDialog = false;
      }
    },
  },
  created: function () {
    evntBus.$on("open_drafts", (data) => {
      this.draftsDialog = true;
      this.dialog_data = data;
    });
  },
};
</script>
