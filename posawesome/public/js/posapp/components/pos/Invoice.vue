<template>
  <div>
    <v-card
      style="max-height: 65vh; height: 65vh"
      class="cards my-0 py-0 grey lighten-5"
    >
      <Customer></Customer>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 55vh">
        <template @mouseover="style = 'cursor: pointer'">
          <v-data-table
            :headers="items_headers"
            :items="items"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            show-expand
            item-key="item_id"
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.amount="{ item }">{{
              (item.qty * item.rate).toFixed(2)
            }}</template>

            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length" class="ma-0 pa-0">
                <v-row class="ma-0 pa-0">
                  <v-col cols="1">
                    <v-btn icon color="red" @click.stop="remove_item(item)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="1">
                    <v-btn
                      icon
                      color="indigo lighten-1"
                      @click.stop="subtract_one(item)"
                    >
                      <v-icon>mdi-minus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="1">
                    <v-btn
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
                      :disabled="item.pricing_rules || !pos_profile.posa_allow_user_to_edit_rate ? true : false"
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
                      :disabled="item.pricing_rules || !pos_profile.posa_allow_user_to_edit_item_discount ? true : false"
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
                      :disabled="item.pricing_rules || !pos_profile.posa_allow_user_to_edit_item_discount ? true : false"
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
                      label="Bacth No"
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
    <v-row>
      <v-col class="pt-0 pr-0" cols="8">
        <v-card
          style="max-height: 25vh; height: 25vh"
          class="cards mb-0 mt-3 py-0 grey lighten-5"
        >
          <v-row no-gutters class="pa-1 pt-2" style="height: 100%">
            <v-col cols="6" no-gutters>
              <v-row no-gutters class="ma-1 pa-0" style="height: 100%">
                <v-col cols="12">
                  <v-text-field
                    v-model="total_qty"
                    label="Total Qty"
                    outlined
                    dense
                    readonly
                    hide-details
                    type="number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="total_items_discount_amount"
                    label="Items Discounts"
                    outlined
                    dense
                    readonly
                    hide-details
                    type="number"
                    :prefix="pos_profile.currency"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="discount_amount"
                    label="ِAdditional Discount"
                    outlined
                    dense
                    hide-details
                    type="number"
                    :prefix="pos_profile.currency"
                    :disabled="!pos_profile.posa_allow_user_to_edit_additional_discount ? true : false"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="subtotal"
                    label="Total"
                    outlined
                    dense
                    readonly
                    hide-details
                    class="text--red"
                    type="number"
                    :prefix="pos_profile.currency"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-col>
            <v-col no-gutters cols="6">
              <v-row no-gutters class="ma-1 pa-0" style="height: 100%">
                <v-col cols="12">
                  <v-text-field
                    v-model="customer_info.email_id"
                    label="Email"
                    outlined
                    dense
                    @change="set_customer_info('email_id', $event)"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="customer_info.mobile_no"
                    label="ِPhone Number"
                    outlined
                    dense
                    hide-details
                    @change="set_customer_info('mobile_no', $event)"
                    type="number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="customer_info.loyalty_program"
                    label="Loyalty Program"
                    outlined
                    dense
                    disabled
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="customer_info.loyalty_points"
                    label="Loyalty Points"
                    outlined
                    dense
                    disabled
                    hide-details
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col class="pt-0 pr-3" cols="4">
        <v-card
          flat
          style="max-height: 25vh; height: 25vh"
          class="cards mb-0 mt-3 py-0"
        >
          <v-row align="start" style="height: 52%">
            <v-col cols="12">
              <v-btn
                block
                class="pa-0"
                large
                color="warning"
                dark
                @click="get_draft_invoices"
                >Get Hold Invoice</v-btn
              >
            </v-col>
            <v-col cols="6">
              <v-btn
                block
                class="pa-0"
                large
                color="error"
                dark
                @click="cancel_invoice"
                >Cancel</v-btn
              >
            </v-col>
            <v-col cols="6">
              <v-btn
                block
                class="pa-0"
                large
                color="success"
                dark
                @click="new_invoice"
                >New</v-btn
              >
            </v-col>
          </v-row>
          <v-row align="end" style="height: 54%">
            <v-col cols="12">
              <v-btn
                block
                class="pa-0"
                large
                color="primary"
                @click="show_payment"
                dark
                >PAY</v-btn
              >
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { evntBus } from "../../bus";
import Customer from "./Customer.vue";
export default {
  // props: ["pos_profile"],
  data() {
    return {
      pos_profile: "",
      pos_opening_shift: "",
      stock_settings: "",
      invoice_doc: "",
      customer: "",
      customer_info: "",
      discount_amount: 0,
      total_tax: 0,
      total: 0,
      items: [],
      itemsPerPage: 1000,
      expanded: [],
      singleExpand: true,
      items_headers: [
        {
          text: "Name",
          align: "start",
          sortable: true,
          value: "item_name",
        },
        { text: "QTY", value: "qty", align: "center" },
        { text: "UOM", value: "uom", align: "center" },
        { text: "Rate", value: "rate", align: "center" },
        { text: "Amount", value: "amount", align: "center" },
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
      const index = this.items.findIndex((el) => el === item);
      this.items.splice(index, 1);
      const idx = this.expanded.findIndex((el) => el === item);
      if (idx >= 0) {
        this.expanded.splice(idx, 1);
      }
    },
    add_one(item) {
      item.qty++;
      this.calc_sotck_gty(item, item.qty);
      // this.$forceUpdate();
    },
    subtract_one(item) {
      item.qty--;
      if (item.qty <= 0) {
        this.remove_item(item);
      }
      this.calc_sotck_gty(item, item.qty);
      // this.$forceUpdate();
    },
    add_item(item) {
      if (!item.uom) {
        item.uom = item.stock_uom;
      }
      const index = this.items.findIndex(
        (el) => el.item_code === item.item_code && el.uom === item.uom
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
            new_item.batch_no = "";
            new_item.batch_no_expiry_date = "";
            new_item.actual_batch_qty = "";
            new_item.qty = item.qty || 1;
            this.items.unshift(new_item);
          }
        }
      }
    },
    get_new_item(item) {
      const new_item = { ...item };
      if (!item.qty) {
        item.qty = 1;
      }
      new_item.stock_qty = item.qty;
      new_item.discount_amount = 0;
      new_item.discount_percentage = 0;
      new_item.discount_amount_per_item = 0;
      new_item.price_list_rate = item.rate;
      new_item.qty = item.qty;
      new_item.uom = item.uom ? item.uom : item.stock_uom;
      new_item.actual_batch_qty = "";
      new_item.conversion_factor = 1;
      new_item.item_id = Date.now();
      if (new_item.has_batch_no || new_item.has_serial_no) {
        this.expanded.push(new_item);
      }
      return new_item;
    },
    cancel_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name && this.pos_profile.posa_allow_delete) {
        frappe.call({
          method: "posawesome.posawesome.api.posapp.delete_invoice",
          args: { invoice: doc.name },
          async: true,
          callback: function (r) {
            if (r.message) {
              evntBus.$emit("show_mesage", {
                text: r.message,
                color: "warning",
              });
            }
          },
        });
      }
      this.items = [];
      this.customer = this.pos_profile.customer;
      this.invoice_doc = "";
      this.discount_amount = 0;
    },
    new_invoice(data = {}) {
      this.expanded = [];
      const doc = this.get_invoice_doc();
      if (doc.name) {
        this.update_invoice(doc);
      } else {
        if (doc.items.length) {
          this.save_draft_invoice(doc);
        }
      }
      if (!data.name) {
        this.items = [];
        this.customer = this.pos_profile.customer;
        this.invoice_doc = "";
        this.discount_amount = 0;
      } else {
        this.invoice_doc = data;
        this.items = data.items;
        let cont = 0;
        this.items.forEach((item) => {
          cont++;
          item.item_id = Date.now() + cont;
        });
        this.update_items_details(this.items);
        this.customer = data.customer;
        this.discount_amount = data.discount_amount;
        this.items.forEach((item) => {
          if (item.serial_no) {
            item.serial_no_selected = [];
            const serial_list = item.serial_no.split("\n");
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
        method: "posawesome.posawesome.api.posapp.save_draft_invoice",
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
      doc.doctype = "Sales Invoice";
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
      return doc;
    },
    get_invoice_items() {
      const items_list = [];
      this.items.forEach((item) => {
        items_list.push({
          item_code: item.item_code,
          qty: item.qty,
          rate: item.rate,
          uom: item.uom,
          conversion_factor: item.conversion_factor,
          serial_no: item.serial_no,
          discount_percentage: item.discount_percentage,
          discount_amount: item.discount_amount,
          batch_no: item.batch_no,
        });
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
          account: "",
        });
      });
      return payments;
    },
    update_invoice(doc) {
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.update_invoice",
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
        evntBus.$emit("show_mesage", {
          text: `There is no Customer !`,
          color: "error",
        });
        return;
      }
      if (!this.items.length) {
        evntBus.$emit("show_mesage", {
          text: `There is no Items !`,
          color: "error",
        });
        return;
      }
      if (!this.validate_items()) {
        return
      }
      evntBus.$emit("show_payment", "true");
      const invoice_doc = this.proces_invoice();
      invoice_doc.customer_info = this.customer_info;
      evntBus.$emit("send_invoice_doc_payment", invoice_doc);
    },
    validate_items() {
      let value = true
      this.items.forEach(item => {
        if (this.pos_profile.update_stock && this.stock_settings.allow_negative_stock != 1) {
          if (item.stock_qty > item.actual_qty) {
            evntBus.$emit("show_mesage", {
              text: `The existing quantity of item ${item.item_name} is not enough`,
              color: "error",
            });
            value = false
          }
        }
        if (item.has_serial_no) {
          if (!item.serial_no_selected || item.stock_qty != item.serial_no_selected.length) {
            evntBus.$emit("show_mesage", {
              text: `Selcted serial numbers of item ${item.item_name} is incorrect`,
              color: "error",
            });
            value = false
          }
        }
        if (item.has_batch_no) {
          if (item.stock_qty > item.actual_batch_qty) {
            evntBus.$emit("show_mesage", {
              text: `The existing batch quantity of item ${item.item_name} is not enough`,
              color: "error",
            });
            value = false
          }
        }
      })
      return value
    },
    get_draft_invoices() {
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_draft_invoices",
        args: {
          pos_opening_shift: this.pos_opening_shift.name,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            evntBus.$emit("open_drafts", r.message);
          }
        },
      });
    },
    close_payments() {
      evntBus.$emit("show_payment", "false");
    },
    update_items_details(items) {
      if (!items.length > 0) {
        return;
      }
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_items_details",
        args: {
          pos_profile: vm.pos_profile,
          items_data: items,
        },
        callback: function (r) {
          if (r.message) {
            items.forEach((item) => {
              const updated_item = r.message.find(
                (element) => element.item_id == item.item_id
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
        method: "posawesome.posawesome.api.posapp.get_item_detail",
        args: {
          doc: this.get_invoice_doc(),
          data: {
            item_code: item.item_code,
            customer: this.customer,
            doctype: "Sales Invoice",
            name: "New Sales Invoice 1",
            company: this.pos_profile.company,
            conversion_rate: 1,
            qty: item.qty,
            price_list_rate: item.price_list_rate,
            child_docname: "New Sales Invoice Item 1",
            cost_center: this.pos_profile.cost_center,
            currency: this.pos_profile.currency,
            // plc_conversion_rate: 1,
            pos_profile: this.pos_profile.name,
            price_list: this.pos_profile.selling_price_list,
            uom: item.uom,
            tax_category: "",
            transaction_type: "selling",
            update_stock: this.pos_profile.update_stock,
          },
        },
        callback: function (r) {
          if (r.message) {
            const data = r.message;
            if (data.has_pricing_rule) {
              item.discount_amount_on_rate = data.discount_amount_on_rate;
              item.discount_percentage = data.discount_percentage;
              item.discount_percentage_on_rate =
                data.discount_percentage_on_rate;
              item.discount_amount = data.discount_amount || 0;
            }
            item.price_list_rate = data.price_list_rate;
            item.has_pricing_rule = data.has_pricing_rule;
            item.last_purchase_rate = data.last_purchase_rate;
            item.price_or_product_discount = data.price_or_product_discount;
            item.pricing_rule_for = data.pricing_rule_for;
            item.pricing_rules = data.pricing_rules;
            item.projected_qty = data.projected_qty;
            item.reserved_qty = data.reserved_qty;
            item.conversion_factor = data.conversion_factor;
            item.stock_qty = data.stock_qty;
            item.stock_uom = data.stock_uom;
            (item.has_serial_no = data.has_serial_no),
              (item.has_batch_no = data.has_batch_no),
              vm.calc_item_price(item);
          }
        },
      });
    },
    fetch_customer_details() {
      const vm = this;
      if (this.customer) {
        return new Promise((resolve) => {
          frappe.db
            .get_value("Customer", vm.customer, [
              "email_id",
              "mobile_no",
              "image",
              "loyalty_program",
            ])
            .then(({ message }) => {
              const { loyalty_program } = message;
              if (loyalty_program) {
                frappe.call({
                  method:
                    "erpnext.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_program_details_with_points",
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
      if (event.target.id === "rate") {
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
      } else if (event.target.id === "discount_amount") {
        if (value < 0) {
          item.discount_amount = 0;
          item.discount_percentage = 0;
        } else {
          item.rate = flt(item.price_list_rate) - flt(value);
          item.discount_percentage = 0;
        }
      } else if (event.target.id === "discount_percentage") {
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
      if (!item.has_pricing_rule) {
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
      } else if (item.pricing_rule_for === "Rate") {
        item.rate = item.price_list_rate;
      }
    },
    calc_uom(item, value) {
      const new_uom = item.item_uoms.find((element) => element.uom == value);
      item.conversion_factor = new_uom.conversion_factor;
      if (!item.has_pricing_rule) {
        item.discount_amount = 0;
        item.discount_percentage = 0;
      }
      this.update_item_detail(item);
    },
    calc_sotck_gty(item, value) {
      item.stock_qty = item.conversion_factor * value;
    },
    set_serial_no(item) {
      item.serial_no = "";
      item.serial_no_selected.forEach((element) => {
        item.serial_no += element + "\n";
      });
      item.serial_no_selected_count = item.serial_no_selected.length;
      if (item.serial_no_selected_count != item.stock_qty) {
        evntBus.$emit("show_mesage", {
          text: `Selected Serial No QTY is ${item.serial_no_selected_count} it should be ${item.stock_qty}`,
          color: "warning",
        });
      }
    },
    set_batch_qty(item, value) {
      const batch_no = item.batch_no_data.find(
        (element) => element.batch_no == value
      );
      item.actual_batch_qty = batch_no.batch_qty;
      item.batch_no_expiry_date = batch_no.expiry_date;
    },
    set_customer_info(field, value) {
      const vm = this;
      frappe.call({
        method:
          "erpnext.selling.page.point_of_sale.point_of_sale.set_customer_info",
        args: {
          fieldname: field,
          customer: this.customer_info.customer,
          value: value,
        },
        callback: (r) => {
          if (!r.exc) {
            vm.customer_info[field] = value;
            evntBus.$emit("show_mesage", {
              text: "Customer contact updated successfully.",
              color: "success",
            });
            frappe.utils.play_sound("submit");
          }
        },
      });
    },
  },
  created() {
    this.$nextTick(function () {});
    evntBus.$on("register_pos_profile", (data) => {
      this.pos_profile = data.pos_profile;
      this.customer = data.pos_profile.customer;
      this.pos_opening_shift = data.pos_opening_shift;
      this.stock_settings = data.stock_settings;
    });
    evntBus.$on("add_item", (item) => {
      // this.expanded = []
      this.add_item(item);
    });
    evntBus.$on("update_customer", (customer) => {
      this.customer = customer;
    });
    evntBus.$on("new_invoice", () => {
      this.invoice_doc = "";
      this.cancel_invoice();
    });
    evntBus.$on("load_invoice", (data) => {
      this.new_invoice(data);
    });
  },
  mounted: function () {},
  watch: {
    customer() {
      this.close_payments();
      evntBus.$emit("set_customer", this.customer);
      this.fetch_customer_details();
    },
    expanded(data_value) {
      this.update_items_details(data_value);
      if (data_value.length > 0) {
        this.update_item_detail(data_value[0]);
      }
    },
  },
};
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
</style>