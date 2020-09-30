<template>
  <v-row justify="center">
    <v-dialog v-model="closingDialog" max-width="900px">
      <v-card>
        <v-card-title>
          <span class="headline">Closing POS Shift</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12" class="pa-1">
                <template>
                  <v-data-table
                    :headers="headers"
                    :items="dialog_data.payment_reconciliation"
                    item-key="mode_of_payment"
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
          <v-btn color="red" dark @click="close_dialog">Close</v-btn>
          <v-btn color="blue" dark @click="submit_dialog">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  data: () => ({
    closingDialog: false,
    singleSelect: true,
    selected: [],
    dialog_data: {},
    headers: [
      {
        text: "Mode of Payment",
        value: "mode_of_payment",
        align: "start",
        sortable: true,
      },
      {
        text: "Opening Amount",
        align: "end",
        sortable: true,
        value: "opening_amount",
      },
      {
        text: "Closing Amount",
        value: "closing_amount",
        align: "end",
        sortable: true,
      },
      {
        text: "Expected Amount",
        value: "expected_amount",
        align: "end",
        sortable: false,
      },
      {
        text: "Difference",
        value: "difference",
        align: "end",
        sortable: false,
      },
    ],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.closingDialog = false;
    },

    submit_dialog() {
      evntBus.$emit("submit_closing_pos", this.dialog_data);
      this.closingDialog = false;
    },
  },
  created: function () {
    evntBus.$on("open_ClosingDialog", (data) => {
      this.closingDialog = true;
      this.dialog_data = data;
    });
  },
};
</script>
