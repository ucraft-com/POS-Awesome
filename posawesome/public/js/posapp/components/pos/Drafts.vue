<template>
  <v-row justify="center">
    <v-dialog v-model="draftsDialog" max-width="900px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" theme="dark" v-bind="attrs" v-on="on">Open Dialog</v-btn>
      </template>-->
      <v-card variant="flat" color="white">
        <v-card-title>
          <span class="text-h5 text-primary">{{
            __('Load Sales Invoice')
            }}</span>
        </v-card-title>
        <v-card-subtitle>
          <span class="text-primary">{{
            __('Load previously saved invoices')
            }}</span>
        </v-card-subtitle>
        <v-card-text class="pa-0">
          <v-container>
            <v-row no-gutters>
              <v-col cols="12" class="pa-1">
                <v-data-table :headers="headers" :items="dialog_data" item-value="name" class="elevation-1" show-select
                  v-model="selected" select-strategy="single" return-object>
                  <template v-slot:item.posting_time="{ item }">
                    {{ item.posting_time.split('.')[0] }}
                  </template>
                  <template v-slot:item.grand_total="{ item }">
                    {{ currencySymbol(item.currency) }}
                    {{ formatCurrency(item.grand_total) }}
                  </template>
                </v-data-table>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" theme="dark" @click="close_dialog">Close</v-btn>
          <v-btn color="success" theme="dark" @click="submit_dialog">Load Sale</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

import format from '../../format';
export default {
  // props: ["draftsDialog"],
  mixins: [format],
  data: () => ({
    draftsDialog: false,
    singleSelect: true,
    selected: [],
    dialog_data: {},
    headers: [
      {
        title: __('Customer'),
        value: 'customer_name',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Date'),
        align: 'start',
        sortable: true,
        value: 'posting_date',
      },
      {
        title: __('Time'),
        align: 'start',
        sortable: true,
        value: 'posting_time',
      },
      {
        title: __('Invoice'),
        value: 'name',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Amount'),
        value: 'grand_total',
        align: 'end',
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
        this.eventBus.emit('load_invoice', this.selected[0]);
        this.draftsDialog = false;
      }
      else {
        this.eventBus.emit("show_message", {
          title: `Select an invoice to load`,
          color: "error",
        });
      }
    },
  },
  created: function () {
    this.eventBus.on('open_drafts', (data) => {
      this.draftsDialog = true;
      this.dialog_data = data;
    });
  },
};
</script>
