<template>
  <div>
    <v-card
      style="max-height: 70vh; height: 70vh"
      class="cards my-0 py-0 grey lighten-5"
    >
      <Customer></Customer>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 60vh">
        <template @mouseover="style = 'cursor: pointer'">
          <v-data-table
            :headers="items_headers"
            :items="items"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            show-expand
            item-key="posa_row_id"
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.qty="{ item }">{{
              formtCurrency(item.qty)
            }}</template>
            <template v-slot:item.rate="{ item }">{{
              formtCurrency(item.rate)
            }}</template>
            <template v-slot:item.amount="{ item }">{{
              formtCurrency(item.qty * item.rate)
            }}</template>
            <template v-slot:item.posa_is_offer="{ item }">
              <v-simple-checkbox
                :value="!!item.posa_is_offer || !!item.posa_is_replace"
                disabled
              ></v-simple-checkbox>
            </template>

            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length" class="ma-0 pa-0">
                <v-row class="ma-0 pa-0">
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="red"
                      @click.stop="remove_item(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="indigo lighten-1"
                      @click.stop="subtract_one(item)"
                    >
                      <v-icon>mdi-minus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="indigo lighten-1"
                      @click.stop="add_one(item)"
                    >
                      <v-icon>mdi-plus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row class="ma-0 pa-0">
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Item Code"
                      background-color="white"
                      hide-details
                      v-model="item.item_code"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="QTY"
                      background-color="white"
                      hide-details
                      v-model.number="item.qty"
                      type="number"
                      @change="calc_sotck_gty(item, $event)"
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      dense
                      background-color="white"
                      label="UOM"
                      v-model="item.uom"
                      :items="item.item_uoms"
                      outlined
                      item-text="uom"
                      item-value="uom"
                      hide-details
                      @change="calc_uom(item, $event)"
                      :disabled="
                        !!invoice_doc.is_return ||
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace
                      "
                    >
                    </v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Rate"
                      background-color="white"
                      hide-details
                      v-model.number="item.rate"
                      type="number"
                      :prefix="invoice_doc.currency"
                      @change="calc_prices(item, $event)"
                      id="rate"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_rate ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Discount Percentage"
                      background-color="white"
                      hide-details
                      v-model.number="item.discount_percentage"
                      type="number"
                      @change="calc_prices(item, $event)"
                      id="discount_percentage"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Discount Amount"
                      background-color="white"
                      hide-details
                      v-model.number="item.discount_amount"
                      type="number"
                      :prefix="invoice_doc.currency"
                      @change="calc_prices(item, $event)"
                      id="discount_amount"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Price list Rate"
                      background-color="white"
                      hide-details
                      v-model="item.price_list_rate"
                      type="number"
                      disabled
                      :prefix="invoice_doc.currency"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Available QTY"
                      background-color="white"
                      hide-details
                      v-model="item.actual_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Group"
                      background-color="white"
                      hide-details
                      v-model="item.item_group"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Stock QTY"
                      background-color="white"
                      hide-details
                      v-model="item.stock_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Stock UOM"
                      background-color="white"
                      hide-details
                      v-model="item.stock_uom"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col align="center" cols="4" v-if="item.posa_offer_applied">
                    <v-checkbox
                      dense
                      label="Offer Applied"
                      v-model="item.posa_offer_applied"
                      readonly
                      hide-details
                      class="shrink mr-2 mt-0"
                    ></v-checkbox>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_serial_no == 1 || item.serial_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Serial No QTY"
                      background-color="white"
                      hide-details
                      v-model="item.serial_no_selected_count"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    v-if="item.has_serial_no == 1 || item.serial_no"
                  >
                    <v-autocomplete
                      v-model="item.serial_no_selected"
                      :items="item.serial_no_data"
                      item-text="serial_no"
                      outlined
                      dense
                      chips
                      color="indigo"
                      small-chips
                      label="Serial No"
                      multiple
                      @change="set_serial_no(item)"
                    ></v-autocomplete>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Batch No Available QTY"
                      background-color="white"
                      hide-details
                      v-model="item.actual_batch_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="Batch No Expiry Date"
                      background-color="white"
                      hide-details
                      v-model="item.batch_no_expiry_date"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="8"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-autocomplete
                      v-model="item.batch_no"
                      :items="item.batch_no_data"
                      item-text="batch_no"
                      outlined
                      dense
                      color="indigo"
                      label="Batch No"
                      @change="set_batch_qty(item, $event)"
                    >
                      <template v-slot:item="data">
                        <template>
                          <v-list-item-content>
                            <v-list-item-title
                              v-html="data.item.batch_no"
                            ></v-list-item-title>
                            <v-list-item-subtitle
                              v-html="
                                `Available QTY  '${data.item.batch_qty}' - Expiry Date ${data.item.expiry_date}`
                              "
                            ></v-list-item-subtitle>
                          </v-list-item-content>
                        </template>
                      </template>
                    </v-autocomplete>
                  </v-col>
                </v-row>
              </td>
            </template>
          </v-data-table>
        </template>
      </div>
    </v-card>
    <v-card class="cards mb-0 mt-3 py-0 grey lighten-5">
      <v-row no-gutters>
        <v-col cols="7">
          <v-row no-gutters class="pa-1 pt-9 pr-1">
            <v-col cols="6" class="pa-1">
              <v-text-field
                :value="formtCurrency(total_qty)"
                label="Total Qty"
                outlined
                dense
                readonly
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-text-field
                v-model="discount_amount"
                label="ِAdditional Discount"
                ref="discount"
                outlined
                dense
                hide-details
                type="number"
                :prefix="pos_profile.currency"
                :disabled="
                  !pos_profile.posa_allow_user_to_edit_additional_discount ||
                  discount_percentage_offer_name
                    ? true
                    : false
                "
              ></v-text-field>
            </v-col>
            <v-col cols="6" class="pa-1 mt-2">
              <v-text-field
                :value="formtCurrency(total_items_discount_amount)"
                label="Items Discounts"
                outlined
                dense
                readonly
                hide-details
                :prefix="pos_profile.currency"
              ></v-text-field>
            </v-col>

            <v-col cols="6" class="pa-1 mt-2">
              <v-text-field
                :value="formtCurrency(subtotal)"
                label="Total"
                outlined
                dense
                readonly
                hide-details
                class="text--red"
                :prefix="pos_profile.currency"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="5">
          <v-row no-gutters class="pa-1 pt-2 pl-0">
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="warning"
                dark
                @click="get_draft_invoices"
                >Hold</v-btn
              >
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                :class="{ 'disable-events': !pos_profile.posa_allow_return }"
                color="info"
                dark
                @click="open_returns"
                >Return</v-btn
              >
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="error"
                dark
                @click="cancel_invoice"
                >Cancel</v-btn
              >
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="success"
                dark
                @click="new_invoice"
                >New</v-btn
              >
            </v-col>
            <v-col cols="12" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="primary"
                @click="show_payment"
                dark
                >PAY</v-btn
              >
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import Customer from './Customer.vue';
export default {
  data() {
    return {
      pos_profile: '',
      pos_opening_shift: '',
      stock_settings: '',
      invoice_doc: '',
      return_doc: '',
      customer: '',
      customer_info: '',
      customer_doc: '',
      discount_amount: 0,
      total_tax: 0,
      items: [],
      posOffers: [],
      posa_offers: [],
      discount_percentage_offer_name: null,
      itemsPerPage: 1000,
      expanded: [],
      singleExpand: true,
      items_headers: [
        {
          text: 'Name',
          align: 'start',
          sortable: true,
          value: 'item_name',
        },
        { text: 'QTY', value: 'qty', align: 'center' },
        { text: 'UOM', value: 'uom', align: 'center' },
        { text: 'Rate', value: 'rate', align: 'center' },
        { text: 'Amount', value: 'amount', align: 'center' },
        { text: 'is Offer', value: 'posa_is_offer', align: 'center' },
      ],
    };
  },

  components: {
    Customer,
  },

  computed: {
    total_qty() {
      this.close_payments();
      let qty = 0;
      this.items.forEach((item) => {
        qty += item.qty;
      });
      return flt(qty).toFixed(2);
    },
    Total() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      return flt(sum).toFixed(2);
    },
    subtotal() {
      this.close_payments();
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      sum -= flt(this.discount_amount);
      return flt(sum).toFixed(2);
    },
    total_items_discount_amount() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.discount_amount;
      });
      return flt(sum).toFixed(2);
    },
  },

  methods: {
    remove_item(item) {
      const index = this.items.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (index >= 0) {
        this.items.splice(index, 1);
      }
      const idx = this.expanded.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (idx >= 0) {
        this.expanded.splice(idx, 1);
      }
    },

    add_one(item) {
      item.qty++;
      if (item.qty == 0) {
        this.remove_item(item);
      }
      this.calc_sotck_gty(item, item.qty);
      this.$forceUpdate();
    },
    subtract_one(item) {
      item.qty--;
      if (item.qty == 0) {
        this.remove_item(item);
      }
      this.calc_sotck_gty(item, item.qty);
      this.$forceUpdate();
    },

    add_item(item) {
      if (!item.uom) {
        item.uom = item.stock_uom;
      }
      const index = this.items.findIndex(
        (el) =>
          el.item_code === item.item_code &&
          el.uom === item.uom &&
          !el.posa_is_offer &&
          !el.posa_is_replace
      );
      if (index === -1) {
        const new_item = this.get_new_item(item);
        this.items.unshift(new_item);
        this.update_item_detail(new_item);
      } else {
        const cur_item = this.items[index];
        this.update_items_details([cur_item]);
        if (!cur_item.has_batch_no) {
          cur_item.qty += item.qty;
          this.calc_sotck_gty(cur_item, cur_item.qty);
        } else {
          if (
            cur_item.stock_qty < cur_item.actual_batch_qty ||
            !cur_item.batch_no
          ) {
            cur_item.qty += item.qty;
            this.calc_sotck_gty(cur_item, cur_item.qty);
          } else {
            const new_item = this.get_new_item(cur_item);
            new_item.batch_no = '';
            new_item.batch_no_expiry_date = '';
            new_item.actual_batch_qty = '';
            new_item.qty = item.qty || 1;
            this.items.unshift(new_item);
          }
        }
      }
      this.$forceUpdate();
    },

    get_new_item(item) {
      const new_item = { ...item };
      if (!item.qty) {
        item.qty = 1;
      }
      if (!item.posa_is_offer) {
        item.posa_is_offer = 0;
      }
      if (!item.posa_is_replace) {
        item.posa_is_replace = '';
      }
      new_item.stock_qty = item.qty;
      new_item.discount_amount = 0;
      new_item.discount_percentage = 0;
      new_item.discount_amount_per_item = 0;
      new_item.price_list_rate = item.rate;
      new_item.qty = item.qty;
      new_item.uom = item.uom ? item.uom : item.stock_uom;
      new_item.actual_batch_qty = '';
      new_item.conversion_factor = 1;
      new_item.posa_offers = JSON.stringify([]);
      new_item.posa_offer_applied = 0;
      new_item.posa_is_offer = item.posa_is_offer;
      new_item.posa_is_replace = item.posa_is_replace || null;
      new_item.is_free_item = 0;
      new_item.posa_row_id = this.makeid(20);
      if (new_item.has_batch_no || new_item.has_serial_no) {
        this.expanded.push(new_item);
      }
      return new_item;
    },

    cancel_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name && this.pos_profile.posa_allow_delete) {
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.delete_invoice',
          args: { invoice: doc.name },
          async: true,
          callback: function (r) {
            if (r.message) {
              evntBus.$emit('show_mesage', {
                text: r.message,
                color: 'warning',
              });
            }
          },
        });
      }
      this.items = [];
      this.posa_offers = [];
      this.customer = this.pos_profile.customer;
      this.invoice_doc = '';
      this.return_doc = '';
      this.discount_amount = 0;
      evntBus.$emit('set_customer_readonly', false);
    },

    new_invoice(data = {}) {
      evntBus.$emit('set_customer_readonly', false);
      this.expanded = [];
      this.posa_offers = [];
      this.return_doc = '';
      const doc = this.get_invoice_doc();
      if (doc.name) {
        this.update_invoice(doc);
      } else {
        if (doc.items.length) {
          this.save_draft_invoice(doc);
        }
      }
      if (!data.name && !data.is_return) {
        this.items = [];
        this.customer = this.pos_profile.customer;
        this.invoice_doc = '';
        this.discount_amount = 0;
      } else {
        if (data.is_return) {
          evntBus.$emit('set_customer_readonly', true);
        }
        this.invoice_doc = data;
        this.items = data.items;
        this.posa_offers = data.posa_offers;
        this.items.forEach((item) => {
          if (!item.posa_row_id) {
            item.posa_row_id = this.makeid(20);
          }
        });
        this.update_items_details(this.items);
        this.customer = data.customer;
        this.discount_amount = data.discount_amount;
        this.items.forEach((item) => {
          if (item.serial_no) {
            item.serial_no_selected = [];
            const serial_list = item.serial_no.split('\n');
            serial_list.forEach((element) => {
              if (element.length) {
                item.serial_no_selected.push(element);
              }
            });
            item.serial_no_selected_count = item.serial_no_selected.length;
          }
        });
      }
    },

    save_draft_invoice() {
      const vm = this;
      const doc = this.get_invoice_doc();
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.save_draft_invoice',
        args: { data: doc },
        async: false,
        callback: function (r) {
          if (r.message) {
            vm.invoice_doc = r.message;
          }
        },
      });
      return this.invoice_doc;
    },

    get_invoice_doc() {
      let doc = {};
      if (this.invoice_doc.name) {
        doc = { ...this.invoice_doc };
      }
      doc.doctype = 'Sales Invoice';
      doc.is_pos = 1;
      doc.company = doc.company || this.pos_profile.company;
      doc.pos_profile = doc.pos_profile || this.pos_profile.name;
      doc.currency = doc.currency || this.pos_profile.currency;
      doc.naming_series = doc.naming_series || this.pos_profile.naming_series;
      doc.customer = this.customer;
      doc.items = this.get_invoice_items();
      doc.total = this.subtotal;
      doc.discount_amount = flt(this.discount_amount);
      doc.posa_pos_opening_shift = this.pos_opening_shift.name;
      doc.payments = this.get_payments();
      doc.taxes = [];
      doc.is_return = this.invoice_doc.is_return;
      doc.return_against = this.invoice_doc.return_against;
      doc.posa_offers = this.posa_offers;
      return doc;
    },

    get_invoice_items() {
      const items_list = [];
      this.items.forEach((item) => {
        const new_item = {
          item_code: item.item_code,
          posa_row_id: item.posa_row_id,
          posa_offers: item.posa_offers,
          posa_offer_applied: item.posa_offer_applied,
          posa_is_offer: item.posa_is_offer,
          posa_is_replace: item.posa_is_replace,
          is_free_item: item.is_free_item,
          qty: item.qty,
          rate: item.rate,
          uom: item.uom,
          amount: item.qty * item.rate,
          conversion_factor: item.conversion_factor,
          serial_no: item.serial_no,
          discount_percentage: item.discount_percentage,
          discount_amount: item.discount_amount,
          batch_no: item.batch_no,
          price_list_rate: item.price_list_rate,
        };
        items_list.push(new_item);
      });

      return items_list;
    },

    get_payments() {
      const payments = [];
      this.pos_profile.payments.forEach((payment) => {
        payments.push({
          amount: 0,
          mode_of_payment: payment.mode_of_payment,
          default: payment.default,
          account: '',
        });
      });
      return payments;
    },

    update_invoice(doc) {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.update_invoice',
        args: {
          data: doc,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            vm.invoice_doc = r.message;
          }
        },
      });
      return this.invoice_doc;
    },

    proces_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name) {
        return this.update_invoice(doc);
      } else {
        return this.save_draft_invoice(doc);
      }
    },

    show_payment() {
      if (!this.customer) {
        evntBus.$emit('show_mesage', {
          text: `There is no Customer !`,
          color: 'error',
        });
        return;
      }
      if (!this.items.length) {
        evntBus.$emit('show_mesage', {
          text: `There is no Items !`,
          color: 'error',
        });
        return;
      }
      if (!this.validate()) {
        return;
      }
      evntBus.$emit('show_payment', 'true');
      const invoice_doc = this.proces_invoice();
      invoice_doc.customer_info = this.customer_info;
      evntBus.$emit('send_invoice_doc_payment', invoice_doc);
    },

    validate() {
      let value = true;
      this.items.forEach((item) => {
        if (
          this.pos_profile.update_stock &&
          this.stock_settings.allow_negative_stock != 1
        ) {
          if (item.is_stock_item && item.stock_qty > item.actual_qty) {
            evntBus.$emit('show_mesage', {
              text: `The existing quantity of item ${item.item_name} is not enough`,
              color: 'error',
            });
            value = false;
          }
        }
        if (
          item.max_discount > 0 &&
          item.discount_percentage > item.max_discount
        ) {
          evntBus.$emit('show_mesage', {
            text: `Maximum discount for Item ${item.item_name} is ${item.max_discount}%`,
            color: 'error',
          });
          value = false;
        }
        if (item.has_serial_no) {
          if (
            !item.serial_no_selected ||
            item.stock_qty != item.serial_no_selected.length
          ) {
            evntBus.$emit('show_mesage', {
              text: `Selcted serial numbers of item ${item.item_name} is incorrect`,
              color: 'error',
            });
            value = false;
          }
        }
        if (item.has_batch_no) {
          if (item.stock_qty > item.actual_batch_qty) {
            evntBus.$emit('show_mesage', {
              text: `The existing batch quantity of item ${item.item_name} is not enough`,
              color: 'error',
            });
            value = false;
          }
        }
        if (this.pos_profile.posa_allow_user_to_edit_additional_discount) {
          const clac_percentage = (this.discount_amount / this.Total) * 100;
          if (clac_percentage > this.pos_profile.posa_max_discount_allowed) {
            evntBus.$emit('show_mesage', {
              text: `The discount should not be higher than ${this.pos_profile.posa_max_discount_allowed}%`,
              color: 'error',
            });
            value = false;
          }
        }
        if (this.invoice_doc.is_return) {
          if (this.subtotal >= 0) {
            evntBus.$emit('show_mesage', {
              text: `Return Invoice Total Not Correct`,
              color: 'error',
            });
            value = false;
            return value;
          }
          if (this.subtotal * -1 > this.return_doc.total) {
            evntBus.$emit('show_mesage', {
              text: `Return Invoice Total should not be higher than ${this.return_doc.total}`,
              color: 'error',
            });
            value = false;
            return value;
          }
          this.items.forEach((item) => {
            const return_item = this.return_doc.items.find(
              (element) => element.item_code == item.item_code
            );

            if (!return_item) {
              evntBus.$emit('show_mesage', {
                text: `The item ${item.item_name} cannot be returned because it is not in the invoice ${this.return_doc.name}`,
                color: 'error',
              });
              value = false;
              return value;
            } else if (item.qty * -1 > return_item.qty || item.qty >= 0) {
              evntBus.$emit('show_mesage', {
                text: `The QTY of the item ${item.item_name} cannot be greater than ${return_item.qty}`,
                color: 'error',
              });
              value = false;
              return value;
            }
          });
        }
      });
      return value;
    },

    get_draft_invoices() {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_draft_invoices',
        args: {
          pos_opening_shift: this.pos_opening_shift.name,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            evntBus.$emit('open_drafts', r.message);
          }
        },
      });
    },

    open_returns() {
      evntBus.$emit('open_returns', this.pos_profile.company);
    },

    close_payments() {
      evntBus.$emit('show_payment', 'false');
    },

    update_items_details(items) {
      if (!items.length > 0) {
        return;
      }
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_items_details',
        args: {
          pos_profile: vm.pos_profile,
          items_data: items,
        },
        callback: function (r) {
          if (r.message) {
            items.forEach((item) => {
              const updated_item = r.message.find(
                (element) => element.posa_row_id == item.posa_row_id
              );
              item.actual_qty = updated_item.actual_qty;
              item.serial_no_data = updated_item.serial_no_data;
              item.batch_no_data = updated_item.batch_no_data;
              item.item_uoms = updated_item.item_uoms;
              item.has_batch_no = updated_item.has_batch_no;
              item.has_serial_no = updated_item.has_serial_no;
            });
          }
        },
      });
    },

    update_item_detail(item) {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_item_detail',
        args: {
          doc: this.get_invoice_doc(),
          data: {
            item_code: item.item_code,
            customer: this.customer,
            doctype: 'Sales Invoice',
            name: 'New Sales Invoice 1',
            company: this.pos_profile.company,
            conversion_rate: 1,
            qty: item.qty,
            price_list_rate: item.price_list_rate,
            child_docname: 'New Sales Invoice Item 1',
            cost_center: this.pos_profile.cost_center,
            currency: this.pos_profile.currency,
            // plc_conversion_rate: 1,
            pos_profile: this.pos_profile.name,
            price_list: this.pos_profile.selling_price_list,
            uom: item.uom,
            tax_category: '',
            transaction_type: 'selling',
            update_stock: this.pos_profile.update_stock,
          },
        },
        callback: function (r) {
          if (r.message) {
            const data = r.message;
            if (data.has_pricing_rule) {
            } else if (
              vm.pos_profile.posa_apply_customer_discount &&
              vm.customer_doc.posa_discount > 0 &&
              vm.customer_doc.posa_discount <= 100
            ) {
              if (
                item.posa_is_offer == 0 &&
                !item.posa_is_replace &&
                item.posa_offer_applied == 0
              ) {
                if (item.max_discount > 0) {
                  item.discount_percentage =
                    item.max_discount < vm.customer_doc.posa_discount
                      ? item.max_discount
                      : vm.customer_doc.posa_discount;
                } else {
                  item.discount_percentage = vm.customer_doc.posa_discount;
                }
              }
            }
            if (!item.btach_price) {
              if (
                !item.is_free_item &&
                !item.posa_is_offer &&
                !item.posa_is_replace
              ) {
                item.price_list_rate = data.price_list_rate;
              }
            }
            item.last_purchase_rate = data.last_purchase_rate;
            item.projected_qty = data.projected_qty;
            item.reserved_qty = data.reserved_qty;
            item.conversion_factor = data.conversion_factor;
            item.stock_qty = data.stock_qty;
            item.actual_qty = data.actual_qty;
            item.stock_uom = data.stock_uom;
            (item.has_serial_no = data.has_serial_no),
              (item.has_batch_no = data.has_batch_no),
              vm.calc_item_price(item);
          }
        },
      });
    },

    fetch_customer_doc() {
      const vm = this;
      if (this.customer) {
        frappe.call({
          method: 'frappe.client.get',
          args: {
            doctype: 'Customer',
            name: vm.customer,
          },
          callback(r) {
            if (r.message) {
              vm.customer_doc = r.message;
            }
          },
        });
      }
    },

    fetch_customer_details() {
      const vm = this;
      if (this.customer) {
        return new Promise((resolve) => {
          frappe.db
            .get_value('Customer', vm.customer, [
              'email_id',
              'mobile_no',
              'image',
              'loyalty_program',
            ])
            .then(({ message }) => {
              const { loyalty_program } = message;
              if (loyalty_program) {
                frappe.call({
                  method:
                    'erpnext.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_program_details_with_points',
                  args: {
                    customer: vm.customer,
                    loyalty_program,
                    silent: true,
                  },
                  callback: (r) => {
                    const { loyalty_points, conversion_factor } = r.message;
                    if (!r.exc) {
                      vm.customer_info = {
                        ...message,
                        customer: vm.customer,
                        loyalty_points,
                        conversion_factor,
                      };
                      resolve();
                    }
                  },
                });
              } else {
                vm.customer_info = { ...message, customer: vm.customer };
                resolve();
              }
            });
        });
      } else {
        return new Promise((resolve) => {
          vm.customer_info = {};
          resolve();
        });
      }
    },

    calc_prices(item, value, $event) {
      if (event.target.id === 'rate') {
        item.discount_percentage = 0;
        if (value < item.price_list_rate) {
          item.discount_amount = (
            flt(item.price_list_rate) - flt(value)
          ).toFixed(2);
        } else if (value < 0) {
          item.rate = item.price_list_rate;
          item.discount_amount = 0;
        } else if (value > item.price_list_rate) {
          item.discount_amount = 0;
        }
      } else if (event.target.id === 'discount_amount') {
        if (value < 0) {
          item.discount_amount = 0;
          item.discount_percentage = 0;
        } else {
          item.rate = flt(item.price_list_rate) - flt(value);
          item.discount_percentage = 0;
        }
      } else if (event.target.id === 'discount_percentage') {
        if (value < 0) {
          item.discount_amount = 0;
          item.discount_percentage = 0;
        } else {
          item.rate = (
            flt(item.price_list_rate) -
            (flt(item.price_list_rate) * flt(value)) / 100
          ).toFixed(2);
          item.discount_amount = (
            flt(item.price_list_rate) - flt(item.rate)
          ).toFixed(2);
        }
      }
    },

    calc_item_price(item) {
      if (!item.posa_offer_applied) {
        if (item.price_list_rate) {
          item.rate = item.price_list_rate;
        }
      }
      if (item.discount_percentage) {
        item.rate =
          flt(item.price_list_rate) -
          (flt(item.price_list_rate) * flt(item.discount_percentage)) / 100;
        item.discount_amount = (
          flt(item.price_list_rate) - flt(item.rate)
        ).toFixed(2);
      } else if (item.discount_amount) {
        item.rate = (
          flt(item.price_list_rate) - flt(item.discount_amount)
        ).toFixed(2);
      }
    },

    calc_uom(item, value) {
      const new_uom = item.item_uoms.find((element) => element.uom == value);
      item.conversion_factor = new_uom.conversion_factor;
      if (!item.posa_offer_applied) {
        item.discount_amount = 0;
        item.discount_percentage = 0;
      }
      if (item.btach_price) {
        item.price_list_rate = item.btach_price * new_uom.conversion_factor;
      }
      this.update_item_detail(item);
    },

    calc_sotck_gty(item, value) {
      item.stock_qty = item.conversion_factor * value;
    },

    set_serial_no(item) {
      item.serial_no = '';
      item.serial_no_selected.forEach((element) => {
        item.serial_no += element + '\n';
      });
      item.serial_no_selected_count = item.serial_no_selected.length;
      if (item.serial_no_selected_count != item.stock_qty) {
        evntBus.$emit('show_mesage', {
          text: `Selected Serial No QTY is ${item.serial_no_selected_count} it should be ${item.stock_qty}`,
          color: 'warning',
        });
      }
    },

    set_batch_qty(item, value) {
      const batch_no = item.batch_no_data.find(
        (element) => element.batch_no == value
      );
      item.actual_batch_qty = batch_no.batch_qty;
      item.batch_no_expiry_date = batch_no.expiry_date;
      if (batch_no.btach_price) {
        item.btach_price = batch_no.btach_price;
        item.price_list_rate = batch_no.btach_price;
        item.rate = batch_no.btach_price;
      } else {
        item.btach_price = null;
        this.update_item_detail(item);
      }
    },

    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },

    shortOpenPayment(e) {
      if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.show_payment();
      }
    },

    shortDeleteFirstItem(e) {
      if (e.key === 'd' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.remove_item(this.items[0]);
      }
    },

    shortOpenFirstItem(e) {
      if (e.key === 'a' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.expanded = [];
        this.expanded.push(this.items[0]);
      }
    },

    shortSelectDiscount(e) {
      if (e.key === 'z' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.$refs.discount.focus();
      }
    },

    makeid(length) {
      let result = '';
      const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
      const charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },

    checkOfferIsAppley(item, offer) {
      let applied = false;
      const item_offers = JSON.parse(item.posa_offers);
      for (const row_id of item_offers) {
        const exist_offer = this.posa_offers.find((el) => row_id == el.row_id);
        if (exist_offer && exist_offer.offer_name == offer.name) {
          applied = true;
          break;
        }
      }
      return applied;
    },

    handelOffers() {
      const itemOffers = this.getItemOffers();
      const groupOffers = this.getGroupOffers();
      const brandOffers = this.getBrandOffers();
      const transactionOffers = this.getTransactionOffers();
      const offers = []
        .concat(itemOffers)
        .concat(groupOffers)
        .concat(brandOffers)
        .concat(transactionOffers);
      this.setItemGiveOffer(offers);
      this.updatePosOffers(offers);
    },

    setItemGiveOffer(offers) {
      // Set item give offer for replace
      offers.forEach((offer) => {
        if (
          offer.apply_on == 'Item Code' &&
          offer.apply_type == 'Item Code' &&
          offer.replace_item
        ) {
          offer.give_item = offer.item;
          offer.apply_item_code = offer.item;
        } else if (
          offer.apply_on == 'Item Group' &&
          offer.apply_type == 'Item Group' &&
          offer.replace_cheapest_item
        ) {
          const offerItemCode = this.getCheapestItem(offer).item_code;
          offer.give_item = offerItemCode;
          offer.apply_item_code = offerItemCode;
        }
      });
    },

    getCheapestItem(offer) {
      let itemsRowID;
      if (typeof offer.items === 'string') {
        itemsRowID = JSON.parse(offer.items);
      } else {
        itemsRowID = offer.items;
      }
      const itemsList = [];
      itemsRowID.forEach((row_id) => {
        itemsList.push(this.getItemFromRowID(row_id));
      });
      const result = itemsList.reduce(function (res, obj) {
        return !obj.posa_is_replace &&
          !obj.posa_is_offer &&
          obj.price_list_rate < res.price_list_rate
          ? obj
          : res;
      });
      return result;
    },

    getItemFromRowID(row_id) {
      const item = this.items.find((el) => el.posa_row_id == row_id);
      return item;
    },

    checkQtyAnountOffer(offer, qty, amount) {
      let min_qty = false;
      let max_qty = false;
      let min_amt = false;
      let max_amt = false;
      const applys = [];

      if (offer.min_qty || offer.min_qty == 0) {
        if (qty >= offer.min_qty) {
          min_qty = true;
        }
        applys.push(min_qty);
      }

      if (offer.max_qty > 0) {
        if (qty <= offer.max_qty) {
          max_qty = true;
        }
        applys.push(max_qty);
      }

      if (offer.min_amt > 0) {
        if (amount >= offer.min_amt) {
          min_amt = true;
        }
        applys.push(min_amt);
      }

      if (offer.max_amt > 0) {
        if (amount <= offer.max_amt) {
          max_amt = true;
        }
        applys.push(max_amt);
      }
      let apply = false;
      if (!applys.includes(false)) {
        apply = true;
      }
      const res = {
        apply: apply,
        conditions: { min_qty, max_qty, min_amt, max_amt },
      };
      return res;
    },

    getItemOffers() {
      const offers = [];
      this.posOffers.forEach((offer) => {
        if (offer.apply_on === 'Item Code') {
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.item_code === offer.item) {
              const items = [];
              if (
                offer.offer === 'Item Price' &&
                item.posa_offer_applied &&
                !this.checkOfferIsAppley(item, offer)
              ) {
              } else {
                const res = this.checkQtyAnountOffer(
                  offer,
                  item.stock_qty,
                  item.stock_qty * item.price_list_rate
                );
                if (res.apply) {
                  items.push(item.posa_row_id);
                  offer.items = items;
                  offers.push(offer);
                }
              }
            }
          });
        }
      });
      return offers;
    },

    getGroupOffers() {
      const offers = [];
      this.posOffers.forEach((offer) => {
        if (offer.apply_on === 'Item Group') {
          const items = [];
          let total_count = 0;
          let total_amount = 0;
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.item_group === offer.item_group) {
              if (
                offer.offer === 'Item Price' &&
                item.posa_offer_applied &&
                !this.checkOfferIsAppley(item, offer)
              ) {
              } else {
                total_count += item.stock_qty;
                total_amount += item.stock_qty * item.price_list_rate;
                items.push(item.posa_row_id);
              }
            }
          });
          if (total_count || total_amount) {
            const res = this.checkQtyAnountOffer(
              offer,
              total_count,
              total_amount
            );
            if (res.apply) {
              offer.items = items;
              offers.push(offer);
            }
          }
        }
      });
      return offers;
    },

    getBrandOffers() {
      const offers = [];
      this.posOffers.forEach((offer) => {
        if (offer.apply_on === 'Brand') {
          const items = [];
          let total_count = 0;
          let total_amount = 0;
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.brand === offer.brand) {
              if (
                offer.offer === 'Item Price' &&
                item.posa_offer_applied &&
                !this.checkOfferIsAppley(item, offer)
              ) {
              } else {
                total_count += item.stock_qty;
                total_amount += item.stock_qty * item.price_list_rate;
                items.push(item.posa_row_id);
              }
            }
          });
          if (total_count || total_amount) {
            const res = this.checkQtyAnountOffer(
              offer,
              total_count,
              total_amount
            );
            if (res.apply) {
              offer.items = items;
              offers.push(offer);
            }
          }
        }
      });
      return offers;
    },
    getTransactionOffers() {
      const offers = [];
      this.posOffers.forEach((offer) => {
        if (offer.apply_on === 'Transaction') {
          let total_qty = 0;
          this.items.forEach((item) => {
            if (!item.posa_is_offer && !item.posa_is_replace) {
              total_qty += item.stock_qty;
            }
          });
          const items = [];
          const total_count = total_qty;
          const total_amount = this.Total;
          if (total_count || total_amount) {
            const res = this.checkQtyAnountOffer(
              offer,
              total_count,
              total_amount
            );
            if (res.apply) {
              this.items.forEach((item) => {
                items.push(item.posa_row_id);
              });
              offer.items = items;
              offers.push(offer);
            }
          }
        }
      });
      return offers;
    },

    updatePosOffers(offers) {
      evntBus.$emit('update_pos_offers', offers);
    },

    updateInvoiceOffers(offers) {
      this.posa_offers.forEach((invoiceOffer) => {
        const existOffer = offers.find(
          (offer) => invoiceOffer.row_id == offer.row_id
        );
        if (!existOffer) {
          this.removeApplyOffer(invoiceOffer);
        }
      });
      offers.forEach((offer) => {
        const existOffer = this.posa_offers.find(
          (invoiceOffer) => invoiceOffer.row_id == offer.row_id
        );
        if (existOffer) {
          existOffer.items = JSON.stringify(offer.items);
          if (
            existOffer.offer === 'Give Product' &&
            existOffer.give_item &&
            existOffer.give_item != offer.give_item
          ) {
            const item_to_remove = this.items.find(
              (item) => item.posa_row_id == existOffer.give_item_row_id
            );
            if (item_to_remove) {
              const updated_item_offers = offer.items.filter(
                (row_id) => row_id != item_to_remove.posa_row_id
              );
              offer.items = updated_item_offers;
              this.remove_item(item_to_remove);
              existOffer.give_item_row_id = null;
              existOffer.give_item = null;
            }
            const newItemOffer = this.ApplyOnGiveProduct(offer);
            if (offer.replace_cheapest_item) {
              const cheapestItem = this.getCheapestItem(offer);
              const oldBaseItem = this.items.find(
                (el) => el.posa_row_id == item_to_remove.posa_is_replace
              );
              newItemOffer.qty = item_to_remove.qty;
              if (oldBaseItem && !oldBaseItem.posa_is_replace) {
                oldBaseItem.qty += item_to_remove.qty;
              } else {
                const restoredItem = this.ApplyOnGiveProduct(
                  {
                    given_qty: item_to_remove.qty,
                  },
                  item_to_remove.item_code
                );
                restoredItem.posa_is_offer = 0;
                this.items.unshift(restoredItem);
              }
              newItemOffer.posa_is_offer = 0;
              newItemOffer.posa_is_replace = cheapestItem.posa_row_id;
              const diffQty = cheapestItem.qty - newItemOffer.qty;
              if (diffQty <= 0) {
                newItemOffer.qty += diffQty;
                this.remove_item(cheapestItem);
                newItemOffer.posa_row_id = cheapestItem.posa_row_id;
                newItemOffer.posa_is_replace = newItemOffer.posa_row_id;
              } else {
                cheapestItem.qty = diffQty;
              }
            }
            this.items.unshift(newItemOffer);
            existOffer.give_item_row_id = newItemOffer.posa_row_id;
            existOffer.give_item = newItemOffer.item_code;
          } else if (
            existOffer.offer === 'Give Product' &&
            existOffer.give_item &&
            existOffer.give_item == offer.give_item &&
            (offer.replace_item || offer.replace_cheapest_item)
          ) {
            this.$nextTick(function () {
              const offerItem = this.getItemFromRowID(
                existOffer.give_item_row_id
              );
              const diff = offer.given_qty - offerItem.qty;
              if (diff > 0) {
                const itemsRowID = JSON.parse(existOffer.items);
                const itemsList = [];
                itemsRowID.forEach((row_id) => {
                  itemsList.push(this.getItemFromRowID(row_id));
                });
                const existItem = itemsList.find(
                  (el) =>
                    el.item_code == offerItem.item_code &&
                    el.posa_is_replace != offerItem.posa_row_id
                );
                if (existItem) {
                  const diffExistQty = existItem.qty - diff;
                  if (diffExistQty > 0) {
                    offerItem.qty += diff;
                    existItem.qty -= diff;
                  } else {
                    offerItem.qty += existItem.qty;
                    this.remove_item(existItem);
                  }
                }
              }
            });
          } else if (existOffer.offer === 'Item Price') {
            this.ApplyOnPrice(offer);
          } else if (existOffer.offer === 'Grand Total') {
            this.ApplyOnTotal(offer);
          }
          this.addOfferToItems(existOffer);
        } else {
          this.applyNewOffer(offer);
        }
      });
    },

    removeApplyOffer(invoiceOffer) {
      if (invoiceOffer.offer === 'Item Price') {
        this.RemoveOnPrice(invoiceOffer);
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      if (invoiceOffer.offer === 'Give Product') {
        const item_to_remove = this.items.find(
          (item) => item.posa_row_id == invoiceOffer.give_item_row_id
        );
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
        this.remove_item(item_to_remove);
      }
      if (invoiceOffer.offer === 'Grand Total') {
        this.RemoveOnTotal(invoiceOffer);
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      if (invoiceOffer.offer === 'Loyalty Point') {
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      this.deleteOfferFromItems(invoiceOffer);
    },

    applyNewOffer(offer) {
      if (offer.offer === 'Item Price') {
        this.ApplyOnPrice(offer);
      }
      if (offer.offer === 'Give Product') {
        let itemsRowID;
        if (typeof offer.items === 'string') {
          itemsRowID = JSON.parse(offer.items);
        } else {
          itemsRowID = offer.items;
        }
        if (
          offer.apply_on == 'Item Code' &&
          offer.apply_type == 'Item Code' &&
          offer.replace_item
        ) {
          const item = this.ApplyOnGiveProduct(offer, offer.item);
          item.posa_is_replace = itemsRowID[0];
          const baseItem = this.items.find(
            (el) => el.posa_row_id == item.posa_is_replace
          );
          const diffQty = baseItem.qty - offer.given_qty;
          item.posa_is_offer = 0;
          if (diffQty <= 0) {
            item.qty = baseItem.qty;
            this.remove_item(baseItem);
            item.posa_row_id = item.posa_is_replace;
          } else {
            baseItem.qty = diffQty;
          }
          this.items.unshift(item);
          offer.give_item_row_id = item.posa_row_id;
        } else if (
          offer.apply_on == 'Item Group' &&
          offer.apply_type == 'Item Group' &&
          offer.replace_cheapest_item
        ) {
          const itemsList = [];
          itemsRowID.forEach((row_id) => {
            itemsList.push(this.getItemFromRowID(row_id));
          });
          const baseItem = itemsList.find(
            (el) => el.item_code == offer.give_item
          );
          const item = this.ApplyOnGiveProduct(offer, offer.give_item);
          item.posa_is_offer = 0;
          item.posa_is_replace = baseItem.posa_row_id;
          const diffQty = baseItem.qty - offer.given_qty;
          if (diffQty <= 0) {
            item.qty = baseItem.qty;
            this.remove_item(baseItem);
            item.posa_row_id = item.posa_is_replace;
          } else {
            baseItem.qty = diffQty;
          }
          this.items.unshift(item);
          offer.give_item_row_id = item.posa_row_id;
        } else {
          const item = this.ApplyOnGiveProduct(offer);
          this.items.unshift(item);
          if (item) {
            offer.give_item_row_id = item.posa_row_id;
          }
        }
      }
      if (offer.offer === 'Grand Total') {
        this.ApplyOnTotal(offer);
      }
      if (offer.offer === 'Loyalty Point') {
        evntBus.$emit('show_mesage', {
          text: 'Loyalty Point Offer Applied',
          color: 'success',
        });
      }

      const newOffer = {
        offer_name: offer.name,
        row_id: offer.row_id,
        apply_on: offer.apply_on,
        offer: offer.offer,
        items: JSON.stringify(offer.items),
        give_item: offer.give_item,
        give_item_row_id: offer.give_item_row_id,
        offer_applied: offer.offer_applied,
      };
      this.posa_offers.push(newOffer);
      this.addOfferToItems(newOffer);
    },

    ApplyOnGiveProduct(offer, item_code) {
      if (!item_code) {
        item_code = offer.give_item;
      }
      const items = JSON.parse(localStorage.getItem('items_storage'));
      const item = items.find((item) => item.item_code == item_code);
      if (!item) {
        return;
      }
      const new_item = { ...item };
      new_item.qty = offer.given_qty;
      new_item.stock_qty = offer.given_qty;
      new_item.rate = offer.discount_type === 'Rate' ? offer.rate : item.rate;
      new_item.discount_amount =
        offer.discount_type === 'Discount Amount' ? offer.discount_amount : 0;
      new_item.discount_percentage =
        offer.discount_type === 'Discount Percentage'
          ? offer.discount_percentage
          : 0;
      new_item.discount_amount_per_item = 0;
      new_item.uom = item.uom ? item.uom : item.stock_uom;
      new_item.actual_batch_qty = '';
      new_item.conversion_factor = 1;
      new_item.posa_offers = JSON.stringify([]);
      new_item.posa_offer_applied = 0;
      new_item.posa_is_offer = 1;
      new_item.posa_is_replace = null;
      new_item.is_free_item =
        (offer.discount_type === 'Rate' && !offer.rate) ||
        (offer.discount_type === 'Discount Percentage' &&
          offer.discount_percentage == 0)
          ? 1
          : 0;
      new_item.posa_row_id = this.makeid(20);
      new_item.price_list_rate =
        (offer.discount_type === 'Rate' && !offer.rate) ||
        (offer.discount_type === 'Discount Percentage' &&
          offer.discount_percentage == 0)
          ? 0
          : item.rate;
      if (new_item.has_batch_no || new_item.has_serial_no) {
        this.expanded.push(new_item);
      }
      this.update_item_detail(new_item);
      return new_item;
    },

    ApplyOnPrice(offer) {
      this.items.forEach((item) => {
        if (offer.items.includes(item.posa_row_id)) {
          const item_offers = JSON.parse(item.posa_offers);
          if (!item_offers.includes(offer.row_id)) {
            if (offer.discount_type === 'Rate') {
              item.rate = offer.rate;
            } else if (offer.discount_type === 'Discount Percentage') {
              item.discount_percentage += offer.discount_percentage;
            } else if (offer.discount_type === 'Discount Amount') {
              item.discount_amount += offer.discount_amount;
            }
            item.posa_offer_applied = 1;
            this.calc_item_price(item);
          }
        }
      });
    },

    RemoveOnPrice(offer) {
      this.items.forEach((item) => {
        const item_offers = JSON.parse(item.posa_offers);
        if (item_offers.includes(offer.row_id)) {
          const originalOffer = this.posOffers.find(
            (el) => el.name == offer.offer_name
          );
          if (originalOffer) {
            if (originalOffer.discount_type === 'Rate') {
              item.rate = item.price_list_rate;
            } else if (originalOffer.discount_type === 'Discount Percentage') {
              item.discount_percentage -= offer.discount_percentage;
              if (!item.discount_percentage) {
                item.discount_percentage = 0;
                item.discount_amount = 0;
                item.rate = item.price_list_rate;
              }
            } else if (originalOffer.discount_type === 'Discount Amount') {
              item.discount_amount -= offer.discount_amount;
            }
            this.calc_item_price(item);
          }
        }
      });
    },

    ApplyOnTotal(offer) {
      if (!offer.name) {
        offer = this.posOffers.find((el) => el.name == offer.offer_name);
      }
      if (
        (!this.discount_percentage_offer_name ||
          this.discount_percentage_offer_name == offer.name) &&
        offer.discount_percentage > 0 &&
        offer.discount_percentage <= 100
      ) {
        this.discount_amount = (
          (flt(this.Total) * flt(offer.discount_percentage)) /
          100
        ).toFixed(2);
        this.discount_percentage_offer_name = offer.name;
      }
    },

    RemoveOnTotal(offer) {
      if (
        this.discount_percentage_offer_name &&
        this.discount_percentage_offer_name == offer.offer_name
      ) {
        this.discount_amount = 0;
        this.discount_percentage_offer_name = null;
      }
    },

    addOfferToItems(offer) {
      const offer_items = JSON.parse(offer.items);
      offer_items.forEach((el) => {
        this.items.forEach((exist_item) => {
          if (exist_item.posa_row_id == el) {
            const item_offers = JSON.parse(exist_item.posa_offers);
            if (!item_offers.includes(offer.row_id)) {
              item_offers.push(offer.row_id);
              if (offer.offer === 'Item Price') {
                exist_item.posa_offer_applied = 1;
              }
            }
            exist_item.posa_offers = JSON.stringify(item_offers);
          }
        });
      });
    },

    deleteOfferFromItems(offer) {
      const offer_items = JSON.parse(offer.items);
      offer_items.forEach((el) => {
        this.items.forEach((exist_item) => {
          if (exist_item.posa_row_id == el) {
            const item_offers = JSON.parse(exist_item.posa_offers);
            const updated_item_offers = item_offers.filter(
              (row_id) => row_id != offer.row_id
            );
            if (offer.offer === 'Item Price') {
              exist_item.posa_offer_applied = 0;
            }
            exist_item.posa_offers = JSON.stringify(updated_item_offers);
          }
        });
      });
    },
  },

  created() {
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
      this.customer = data.pos_profile.customer;
      this.pos_opening_shift = data.pos_opening_shift;
      this.stock_settings = data.stock_settings;
    });
    evntBus.$on('add_item', (item) => {
      this.add_item(item);
    });
    evntBus.$on('update_customer', (customer) => {
      this.customer = customer;
    });
    evntBus.$on('new_invoice', () => {
      this.invoice_doc = '';
      this.cancel_invoice();
    });
    evntBus.$on('load_invoice', (data) => {
      this.new_invoice(data);
    });
    evntBus.$on('set_offers', (data) => {
      this.posOffers = data;
    });
    evntBus.$on('update_invoice_offers', (data) => {
      this.updateInvoiceOffers(data);
    });
    evntBus.$on('load_return_invoice', (data) => {
      this.new_invoice(data.invoice_doc);
      this.discount_amount = -data.return_doc.discount_amount;
      this.return_doc = data.return_doc;
    });
    document.addEventListener('keydown', this.shortOpenPayment.bind(this));
    document.addEventListener('keydown', this.shortDeleteFirstItem.bind(this));
    document.addEventListener('keydown', this.shortOpenFirstItem.bind(this));
    document.addEventListener('keydown', this.shortSelectDiscount.bind(this));
  },
  destroyed() {
    document.removeEventListener('keydown', this.shortOpenPayment);
    document.removeEventListener('keydown', this.shortDeleteFirstItem);
    document.removeEventListener('keydown', this.shortOpenFirstItem);
    document.removeEventListener('keydown', this.shortSelectDiscount);
  },
  watch: {
    customer() {
      this.close_payments();
      evntBus.$emit('set_customer', this.customer);
      this.fetch_customer_doc();
      this.fetch_customer_details();
    },
    customer_info() {
      evntBus.$emit('set_customer_info_to_edit', this.customer_info);
    },
    expanded(data_value) {
      this.update_items_details(data_value);
      if (data_value.length > 0) {
        this.update_item_detail(data_value[0]);
      }
    },
    discount_percentage_offer_name() {
      evntBus.$emit('update_discount_percentage_offer_name', {
        value: this.discount_percentage_offer_name,
      });
    },
    items: {
      deep: true,
      handler(items) {
        this.handelOffers();
        this.$forceUpdate();
      },
    },
  },
};
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
.disable-events {
  pointer-events: none;
}
</style>