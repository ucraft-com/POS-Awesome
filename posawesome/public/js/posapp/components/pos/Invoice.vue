<template>
  <div>
    <v-dialog v-model="cancel_dialog" max-width="330">
      <v-card>
        <v-card-title class="text-h5">
          <span class="text-h5 text-primary">{{
            __("Cancel Sale ?")
            }}</span>
        </v-card-title>
        <v-card-text>
          This would cancel and delete the current sale. To save it as Draft, click the "Save and Clear" instead.
        </v-card-text>
        <!-- <v-card- -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="cancel_invoice">
            {{ __("Yes, Cancel sale") }}
          </v-btn>
          <v-btn color="warning" @click="cancel_dialog = false">
            {{ __("Back") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-card style="max-height: 70vh; height: 70vh" class="cards my-0 py-0 mt-3 bg-grey-lighten-5">
      <v-row align="center" class="items px-2 py-1">
        <v-col v-if="pos_profile.posa_allow_sales_order" cols="9" class="pb-2 pr-0">
          <Customer></Customer>
        </v-col>
        <v-col v-if="!pos_profile.posa_allow_sales_order" cols="12" class="pb-2">
          <Customer></Customer>
        </v-col>
        <v-col v-if="pos_profile.posa_allow_sales_order" cols="3" class="pb-2">
          <v-select density="compact" hide-details variant="outlined" color="primary" bg-color="white"
            :items="invoiceTypes" :label="frappe._('Type')" v-model="invoiceType"
            :disabled="invoiceType == 'Return'"></v-select>
        </v-col>
      </v-row>

      <v-row align="center" class="items px-2 py-1 mt-0 pt-0" v-if="pos_profile.posa_use_delivery_charges">
        <v-col cols="8" class="pb-0 mb-0 pr-0 pt-0">
          <v-autocomplete density="compact" clearable auto-select-first variant="outlined" color="primary"
            :label="frappe._('Delivery Charges')" v-model="selected_delivery_charge" :items="delivery_charges"
            item-title="name" item-value="name" return-object bg-color="white" :no-data-text="__('Charges not found')"
            hide-details :customFilter="deliveryChargesFilter" :disabled="readonly"
            @update:model-value="update_delivery_charges()">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <v-list-item-title class="text-primary text-subtitle-1" v-html="item.raw.name"></v-list-item-title>
                <v-list-item-subtitle v-html="`Rate: ${item.raw.rate}`"></v-list-item-subtitle>
              </v-list-item>
            </template>
          </v-autocomplete>
        </v-col>
        <v-col cols="4" class="pb-0 mb-0 pt-0">
          <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Delivery Charges Rate')"
            bg-color="white" hide-details :model-value="formatCurrency(delivery_charges_rate)"
            :prefix="currencySymbol(pos_profile.currency)" disabled></v-text-field>
        </v-col>
      </v-row>
      <v-row align="center" class="items px-2 py-1 mt-0 pt-0" v-if="pos_profile.posa_allow_change_posting_date">
        <v-col v-if="pos_profile.posa_allow_change_posting_date" cols="4" class="pb-2">
          <v-menu ref="invoice_posting_date" v-model="invoice_posting_date" :close-on-content-click="false"
            transition="scale-transition" density="default">
            <template v-slot:activator="{ props }">
              <v-text-field v-model="posting_date" :label="frappe._('Posting Date')" readonly variant="outlined"
                density="compact" bg-color="white" clearable color="primary" hide-details v-bind="props"></v-text-field>
            </template>
            <v-date-picker v-model="posting_date" no-title scrollable color="primary" :min="frappe.datetime.add_days(frappe.datetime.now_date(true), -7)
              " :max="frappe.datetime.add_days(frappe.datetime.now_date(true), 7)"
              @input="invoice_posting_date = false">
            </v-date-picker>
          </v-menu>
        </v-col>
      </v-row>

      <div class="my-0 py-0 overflow-y-auto" style="max-height: 60vh">
        <v-data-table :headers="items_headers" :items="items" v-model:expanded="expanded" show-expand
          item-value="posa_row_id" class="elevation-1" :items-per-page="itemsPerPage" expand-on-click
          hide-default-footer>
          <template v-slot:item.qty="{ item }">{{
            formatFloat(item.qty)
          }}</template>
          <template v-slot:item.rate="{ item }">{{ currencySymbol(pos_profile.currency) }}
            {{ formatCurrency(item.rate) }}</template>
          <template v-slot:item.amount="{ item }">{{ currencySymbol(pos_profile.currency) }}
            {{
              formatCurrency(
                flt(item.qty, float_precision) *
                flt(item.rate, currency_precision)
              )
            }}</template>
          <template v-slot:item.posa_is_offer="{ item }">
            <v-checkbox-btn :model-value="!!item.posa_is_offer || !!item.posa_is_replace" class="center"
              disabled></v-checkbox-btn>
          </template>

          <template v-slot:expanded-row="{ columns: headers, item }">
            <td :colspan="headers.length" class="ma-0 pa-0">
              <v-row class="ma-0 pa-0">
                <v-col cols="1">
                  <v-btn :disabled="!!item.posa_is_offer || !!item.posa_is_replace" icon color="error"
                    @click.stop="remove_item(item)">
                    <v-icon icon="mdi-delete">mdi-delete</v-icon>
                  </v-btn>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="1">
                  <v-btn :disabled="!!item.posa_is_offer || !!item.posa_is_replace" icon color="secondary"
                    @click.stop="subtract_one(item)">
                    <v-icon icon="mdi-minus-circle-outline"></v-icon>
                  </v-btn>
                </v-col>
                <v-col cols="1">
                  <v-btn :disabled="!!item.posa_is_offer || !!item.posa_is_replace" icon color="secondary"
                    @click.stop="add_one(item)">
                    <v-icon icon="mdi-plus-circle-outline"></v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row class="ma-0 pa-0">
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Item Code')"
                    bg-color="white" hide-details v-model="item.item_code" disabled></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('QTY')"
                    bg-color="white" hide-details :model-value="formatFloat(item.qty)" @change="
                      [
                        setFormatedFloat(item, 'qty', null, false, $event),
                        calc_stock_qty(item, $event),
                      ]
                      " :rules="[isNumber]" :disabled="!!item.posa_is_offer || !!item.posa_is_replace"></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-select density="compact" bg-color="white" :label="frappe._('UOM')" v-model="item.uom"
                    :items="item.item_uoms" variant="outlined" item-title="uom" item-value="uom" hide-details
                    @update:model-value="calc_uom(item, $event)" :disabled="!!invoice_doc.is_return ||
                      !!item.posa_is_offer ||
                      !!item.posa_is_replace
                      ">
                  </v-select>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Rate')"
                    bg-color="white" hide-details :prefix="currencySymbol(pos_profile.currency)"
                    :model-value="formatCurrency(item.rate)" @change="
                      [
                        setFormatedCurrency(
                          item,
                          'rate',
                          null,
                          false,
                          $event
                        ),
                        calc_prices(item, $event),
                      ]
                      " :rules="[isNumber]" id="rate" :disabled="!!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_rate ||
                        !!invoice_doc.is_return
                        ? true
                        : false
                        "></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary"
                    :label="frappe._('Discount Percentage')" bg-color="white" hide-details
                    :model-value="formatFloat(item.discount_percentage)" @change="
                      [
                        setFormatedCurrency(
                          item,
                          'discount_percentage',
                          null,
                          true,
                          $event
                        ),
                        calc_prices(item, $event),
                      ]
                      " :rules="[isNumber]" id="discount_percentage" :disabled="!!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                        ? true
                        : false
                        " suffix="%"></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary"
                    :label="frappe._('Discount Amount')" bg-color="white" hide-details
                    :model-value="formatCurrency(item.discount_amount)" :rules="[isNumber]" @change="
                      [
                        setFormatedCurrency(
                          item,
                          'discount_amount',
                          null,
                          true,
                          $event
                        ),
                        ,
                        calc_prices(item, $event),
                      ]
                      " :prefix="currencySymbol(pos_profile.currency)" id="discount_amount" :disabled="!!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                        ? true
                        : false
                        "></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary"
                    :label="frappe._('Price list Rate')" bg-color="white" hide-details
                    :model-value="formatCurrency(item.price_list_rate)" disabled
                    :prefix="currencySymbol(pos_profile.currency)"></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Available QTY')"
                    bg-color="white" hide-details :model-value="formatFloat(item.actual_qty)" disabled></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Group')"
                    bg-color="white" hide-details v-model="item.item_group" disabled></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Stock QTY')"
                    bg-color="white" hide-details :model-value="formatFloat(item.stock_qty)" disabled></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Stock UOM')"
                    bg-color="white" hide-details v-model="item.stock_uom" disabled></v-text-field>
                </v-col>
                <v-col align="center" cols="4" v-if="item.posa_offer_applied">
                  <v-checkbox density="default" :label="frappe._('Offer Applied')" v-model="item.posa_offer_applied"
                    readonly hide-details class="shrink mr-2 mt-0"></v-checkbox>
                </v-col>
                <v-col cols="4" v-if="item.has_serial_no == 1 || item.serial_no">
                  <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Serial No QTY')"
                    bg-color="white" hide-details v-model="item.serial_no_selected_count" type="number"
                    disabled></v-text-field>
                </v-col>
                <v-col cols="12" v-if="item.has_serial_no == 1 || item.serial_no">
                  <v-autocomplete v-model="item.serial_no_selected" :items="item.serial_no_data" item-title="serial_no"
                    variant="outlined" density="compact" chips color="primary" small-chips
                    :label="frappe._('Serial No')" multiple @update:model-value="set_serial_no(item)"></v-autocomplete>
                </v-col>
                <v-col cols="4" v-if="item.has_batch_no == 1 || item.batch_no">
                  <v-text-field density="compact" variant="outlined" color="primary"
                    :label="frappe._('Batch No. Available QTY')" bg-color="white" hide-details
                    :model-value="formatFloat(item.actual_batch_qty)" disabled></v-text-field>
                </v-col>
                <v-col cols="4" v-if="item.has_batch_no == 1 || item.batch_no">
                  <v-text-field density="compact" variant="outlined" color="primary"
                    :label="frappe._('Batch No Expiry Date')" bg-color="white" hide-details
                    v-model="item.batch_no_expiry_date" disabled></v-text-field>
                </v-col>
                <v-col cols="8" v-if="item.has_batch_no == 1 || item.batch_no">
                  <v-autocomplete v-model="item.batch_no" :items="item.batch_no_data" item-title="batch_no"
                    variant="outlined" density="compact" color="primary" :label="frappe._('Batch No')"
                    @update:model-value="set_batch_qty(item, $event)">
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props">
                        <v-list-item-title v-html="item.raw.batch_no"></v-list-item-title>
                        <v-list-item-subtitle v-html="`Available QTY  '${item.raw.batch_qty}' - Expiry Date ${item.raw.expiry_date}`
                          "></v-list-item-subtitle>

                      </v-list-item>
                    </template>
                  </v-autocomplete>
                </v-col>
                <v-col cols="4" v-if="
                  pos_profile.posa_allow_sales_order &&
                  invoiceType == 'Order'
                ">
                  <v-menu ref="item_delivery_date" v-model="item.item_delivery_date" :close-on-content-click="false"
                    v-model:return-value="item.posa_delivery_date" transition="scale-transition" density="default">
                    <template v-slot:activator="{ props }">
                      <v-text-field v-model="item.posa_delivery_date" :label="frappe._('Delivery Date')" readonly
                        variant="outlined" density="compact" clearable color="primary" hide-details
                        v-bind="props"></v-text-field>
                    </template>
                    <v-date-picker v-model="item.posa_delivery_date" no-title scrollable color="primary"
                      :min="frappe.datetime.now_date()">
                      <v-spacer></v-spacer>
                      <v-btn variant="text" color="primary" @click="item.item_delivery_date = false">
                        Cancel
                      </v-btn>
                      <v-btn variant="text" color="primary" @click="
                        [
                          $refs.item_delivery_date.save(
                            item.posa_delivery_date
                          ),
                          validate_due_date(item),
                        ]
                        ">
                        OK
                      </v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-col cols="8" v-if="pos_profile.posa_display_additional_notes">
                  <v-textarea class="pa-0" variant="outlined" density="compact" clearable color="primary" auto-grow
                    rows="1" :label="frappe._('Additional Notes')" v-model="item.posa_notes"
                    :model-value="item.posa_notes"></v-textarea>
                </v-col>
              </v-row>
            </td>
          </template>
        </v-data-table>
      </div>
    </v-card>
    <v-card class="cards mb-0 mt-3 py-0 bg-grey-lighten-5">
      <v-row no-gutters>
        <v-col cols="7">
          <v-row no-gutters class="pa-1 pt-9 pr-1">
            <v-col cols="6" class="pa-1">
              <v-text-field :model-value="formatFloat(total_qty)" :label="frappe._('Total Qty')" variant="outlined"
                density="compact" readonly hide-details color="accent"></v-text-field>
            </v-col>
            <v-col v-if="!pos_profile.posa_use_percentage_discount" cols="6" class="pa-1">
              <v-text-field :model-value="formatCurrency(discount_amount)" @change="
                setFormatedCurrency(
                  discount_amount,
                  'discount_amount',
                  null,
                  false,
                  $event
                )
                " :rules="[isNumber]" :label="frappe._('Additional Discount')" ref="discount" variant="outlined"
                density="compact" hide-details color="warning" :prefix="currencySymbol(pos_profile.currency)" :disabled="!pos_profile.posa_allow_user_to_edit_additional_discount ||
                  discount_percentage_offer_name
                  ? true
                  : false
                  "></v-text-field>
            </v-col>
            <v-col v-if="pos_profile.posa_use_percentage_discount" cols="6" class="pa-1">
              <v-text-field :model-value="formatFloat(additional_discount_percentage)" @change="
                [
                  setFormatedFloat(
                    additional_discount_percentage,
                    'additional_discount_percentage',
                    null,
                    false,
                    $event
                  ),
                  update_discount_umount(),
                ]
                " :rules="[isNumber]" :label="frappe._('Additional Discount %')" suffix="%" ref="percentage_discount"
                variant="outlined" density="compact" color="warning" hide-details :disabled="!pos_profile.posa_allow_user_to_edit_additional_discount ||
                  discount_percentage_offer_name
                  ? true
                  : false
                  "></v-text-field>
            </v-col>
            <v-col cols="6" class="pa-1 mt-2">
              <v-text-field :model-value="formatCurrency(total_items_discount_amount)"
                :prefix="currencySymbol(pos_profile.currency)" :label="frappe._('Items Discounts')" variant="outlined"
                density="compact" color="warning" readonly hide-details></v-text-field>
            </v-col>

            <v-col cols="6" class="pa-1 mt-2">
              <v-text-field :model-value="formatCurrency(subtotal)" :prefix="currencySymbol(pos_profile.currency)"
                :label="frappe._('Total')" variant="outlined" density="compact" readonly hide-details
                color="success"></v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="5">
          <v-row no-gutters class="pa-1 pt-2 pl-0">
            <v-col cols="6" class="pa-1">
              <v-btn block class="pa-0" color="accent" theme="dark" @click="save_and_clear_invoice">
                {{ __("Save and Clear") }}</v-btn>
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn block class="pa-0" color="warning" theme="dark" @click="get_draft_invoices">{{
                __("Load Draft sales")
                }}</v-btn>
            </v-col>
            <v-col v-if="pos_profile.custom_allow_select_sales_order === 1" cols="6" class="pa-1">
              <v-btn block class="pa-0" color="info" theme="dark" @click="get_draft_orders">{{ __("Select S.O")
                }}</v-btn>
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn block class="pa-0" color="error" theme="dark" @click="cancel_dialog = true">{{ __("Cancel Sale")
                }}</v-btn>
            </v-col>
            <v-col v-if="pos_profile.posa_allow_return == 1" cols="6" class="pa-1">
              <v-btn block class="pa-0" :class="{ 'disable-events': !pos_profile.posa_allow_return }" color="secondary"
                theme="dark" @click="open_returns">{{ __("Sales Return") }}</v-btn>
            </v-col>

            <v-col class="pa-1">
              <v-btn block class="pa-0" color="success" @click="show_payment" theme="dark">{{ __("PAY") }}</v-btn>
            </v-col>
            <v-col v-if="pos_profile.posa_allow_print_draft_invoices" cols="6" class="pa-1">
              <v-btn block class="pa-0" color="primary" @click="print_draft_invoice" theme="dark">{{ __("Print Draft")
                }}</v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>

import format from "../../format";
import Customer from "./Customer.vue";

export default {
  mixins: [format],
  data() {
    return {
      pos_profile: "",
      pos_opening_shift: "",
      stock_settings: "",
      invoice_doc: "",
      return_doc: "",
      customer: "",
      customer_info: "",
      discount_amount: 0,
      additional_discount_percentage: 0,
      total_tax: 0,
      items: [],
      posOffers: [],
      posa_offers: [],
      posa_coupons: [],
      allItems: [],
      discount_percentage_offer_name: null,
      invoiceTypes: ["Invoice", "Order"],
      invoiceType: "Invoice",
      itemsPerPage: 1000,
      expanded: [],
      singleExpand: true,
      cancel_dialog: false,
      float_precision: 2,
      currency_precision: 2,
      new_line: false,
      delivery_charges: [],
      delivery_charges_rate: 0,
      selected_delivery_charge: "",
      invoice_posting_date: false,
      posting_date: frappe.datetime.nowdate(),
      items_headers: [
        {
          title: __("Name"),
          align: "start",
          sortable: true,
          key: "item_name",
        },
        { title: __("QTY"), key: "qty", align: "center" },
        { title: __("UOM"), key: "uom", align: "center" },
        { title: __("Rate"), key: "rate", align: "center" },
        { title: __("Amount"), key: "amount", align: "center" },
        { title: __("Offer?"), key: "posa_is_offer", align: "center" },
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
        qty += flt(item.qty);
      });
      return this.flt(qty, this.float_precision);
    },
    Total() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += flt(item.qty) * flt(item.rate);
      });
      return this.flt(sum, this.currency_precision);
    },
    subtotal() {
      this.close_payments();
      let sum = 0;
      this.items.forEach((item) => {
        sum += flt(item.qty) * flt(item.rate);
      });
      sum -= this.flt(this.discount_amount);
      sum += this.flt(this.delivery_charges_rate);
      return this.flt(sum, this.currency_precision);
    },
    total_items_discount_amount() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += flt(item.qty) * flt(item.discount_amount);
      });
      return this.flt(sum, this.float_precision);
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
      this.calc_stock_qty(item, item.qty);
      this.$forceUpdate();
    },
    subtract_one(item) {
      item.qty--;
      if (item.qty == 0) {
        this.remove_item(item);
      }
      this.calc_stock_qty(item, item.qty);
      this.$forceUpdate();
    },

    add_item(item) {
      if (!item.uom) {
        item.uom = item.stock_uom;
      }
      let index = -1;
      if (!this.new_line) {
        index = this.items.findIndex(
          (el) =>
            el.item_code === item.item_code &&
            el.uom === item.uom &&
            !el.posa_is_offer &&
            !el.posa_is_replace &&
            el.batch_no === item.batch_no
        );
      }
      if (index === -1 || this.new_line) {
        const new_item = this.get_new_item(item);
        if (item.has_serial_no && item.to_set_serial_no) {
          new_item.serial_no_selected = [];
          new_item.serial_no_selected.push(item.to_set_serial_no);
          item.to_set_serial_no = null;
        }
        if (item.has_batch_no && item.to_set_batch_no) {
          new_item.batch_no = item.to_set_batch_no;
          item.to_set_batch_no = null;
          item.batch_no = null;
          this.set_batch_qty(new_item, new_item.batch_no, false);
        }
        this.items.unshift(new_item);
        this.update_item_detail(new_item);
      } else {
        const cur_item = this.items[index];
        this.update_items_details([cur_item]);
        if (item.has_serial_no && item.to_set_serial_no) {
          if (cur_item.serial_no_selected.includes(item.to_set_serial_no)) {
            this.eventBus.emit("show_message", {
              title: __(`This Serial Number {0} has already been added!`, [
                item.to_set_serial_no,
              ]),
              color: "warning",
            });
            item.to_set_serial_no = null;
            return;
          }
          cur_item.serial_no_selected.push(item.to_set_serial_no);
          item.to_set_serial_no = null;
        }
        if (!cur_item.has_batch_no) {
          cur_item.qty += item.qty || 1;
          this.calc_stock_qty(cur_item, cur_item.qty);
        } else {
          if (
            (cur_item.stock_qty < cur_item.actual_batch_qty &&
              cur_item.batch_no == item.batch_no) ||
            !cur_item.batch_no
          ) {
            cur_item.qty += item.qty || 1;
            this.calc_stock_qty(cur_item, cur_item.qty);
          } else {
            const new_item = this.get_new_item(cur_item);
            new_item.batch_no = item.batch_no || item.to_set_batch_no;
            new_item.batch_no_expiry_date = "";
            new_item.actual_batch_qty = "";
            new_item.qty = item.qty || 1;
            if (new_item.batch_no) {
              this.set_batch_qty(new_item, new_item.batch_no, false);
              item.to_set_batch_no = null;
              item.batch_no = null;
            }
            this.items.unshift(new_item);
          }
        }
        this.set_serial_no(cur_item);
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
        item.posa_is_replace = "";
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
      new_item.posa_offers = JSON.stringify([]);
      new_item.posa_offer_applied = 0;
      new_item.posa_is_offer = item.posa_is_offer;
      new_item.posa_is_replace = item.posa_is_replace || null;
      new_item.is_free_item = 0;
      new_item.posa_notes = "";
      new_item.posa_delivery_date = "";
      new_item.posa_row_id = this.makeid(20);
      if (
        (!this.pos_profile.posa_auto_set_batch && new_item.has_batch_no) ||
        new_item.has_serial_no
      ) {
        this.expanded.push(new_item);
      }
      return new_item;
    },

    clear_invoice() {
      this.items = [];
      this.posa_offers = [];
      this.expanded = [];
      this.posa_offers = [];
      this.eventBus.emit("set_pos_coupons", []);
      this.posa_coupons = [];
      this.customer = this.pos_profile.customer;
      this.invoice_doc = "";
      this.return_doc = "";
      this.discount_amount = 0;
      this.additional_discount_percentage = 0;
      this.delivery_charges_rate = 0;
      this.selected_delivery_charge = "";
      this.eventBus.emit("set_customer_readonly", false);
      this.invoiceType = this.pos_profile.posa_default_sales_order
        ? "Order"
        : "Invoice";
      this.invoiceTypes = ["Invoice", "Order"];
    },

    async cancel_invoice() {
      const doc = this.get_invoice_doc();
      this.invoiceType = this.pos_profile.posa_default_sales_order
        ? "Order"
        : "Invoice";
      this.invoiceTypes = ["Invoice", "Order"];
      this.posting_date = frappe.datetime.nowdate();
      var vm = this;
      if (doc.name && this.pos_profile.posa_allow_delete) {
        await frappe.call({
          method: "posawesome.posawesome.api.posapp.delete_invoice",
          args: { invoice: doc.name },
          async: true,
          callback: function (r) {
            if (r.message) {
              vm.eventBus.emit("show_message", {
                text: r.message,
                color: "warning",
              });
            }
          },
        });
      }
      this.clear_invoice()
      this.cancel_dialog = false;
    },

    async load_invoice(data = {}) {
      this.clear_invoice()
      if (data.is_return) {
        this.eventBus.emit("set_customer_readonly", true);
        this.invoiceType = "Return";
        this.invoiceTypes = ["Return"];
      }
      this.invoice_doc = data;
      this.items = data.items;
      this.update_items_details(this.items);
      this.posa_offers = data.posa_offers || [];
      this.items.forEach((item) => {
        if (!item.posa_row_id) {
          item.posa_row_id = this.makeid(20);
        }
        if (item.batch_no) {
          this.set_batch_qty(item, item.batch_no);
        }
      });
      this.customer = data.customer;
      this.posting_date = data.posting_date || frappe.datetime.nowdate();
      this.discount_amount = data.discount_amount;
      this.additional_discount_percentage =
        data.additional_discount_percentage;
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
      if (data.is_return) {
        this.discount_amount = -data.discount_amount;
        this.additional_discount_percentage =
          -data.additional_discount_percentage;
        this.return_doc = data;
      } else {
        this.eventBus.emit("set_pos_coupons", data.posa_coupons);
      }
    },
    save_and_clear_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name) {
        old_invoice = this.update_invoice(doc);
      } else {
        if (doc.items.length) {
          old_invoice = this.update_invoice(doc);
        }
        else {
          this.eventBus.emit("show_message", {
            title: `Nothing to save`,
            color: "error",
          });
        }
      }
      if (!old_invoice) {
        this.eventBus.emit("show_message", {
          title: `Error saving the current invoice`,
          color: "error",
        });
      }
      else {
        this.clear_invoice();
        return old_invoice;
      }

    },

    async new_order(data = {}) {
      let old_invoice = null;
      this.eventBus.emit("set_customer_readonly", false);
      this.expanded = [];
      this.posa_offers = [];
      this.eventBus.emit("set_pos_coupons", []);
      this.posa_coupons = [];
      this.return_doc = "";
      if (!data.name && !data.is_return) {
        this.items = [];
        this.customer = this.pos_profile.customer;
        this.invoice_doc = "";
        this.discount_amount = 0;
        this.additional_discount_percentage = 0;
        this.invoiceType = "Invoice";
        this.invoiceTypes = ["Invoice", "Order"];
      } else {
        if (data.is_return) {
          this.eventBus.emit("set_customer_readonly", true);
          this.invoiceType = "Return";
          this.invoiceTypes = ["Return"];
        }
        this.invoice_doc = data;
        this.items = data.items;
        this.update_items_details(this.items);
        this.posa_offers = data.posa_offers || [];
        this.items.forEach((item) => {
          if (!item.posa_row_id) {
            item.posa_row_id = this.makeid(20);
          }
          if (item.batch_no) {
            this.set_batch_qty(item, item.batch_no);
          }
        });
        this.customer = data.customer;
        this.posting_date = data.posting_date || frappe.datetime.nowdate();
        this.discount_amount = data.discount_amount;
        this.additional_discount_percentage =
          data.additional_discount_percentage;
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
      return old_invoice;
    },

    get_invoice_doc() {
      let doc = {};
      if (this.invoice_doc.name) {
        doc = { ...this.invoice_doc };
      }
      doc.doctype = "Sales Invoice";
      doc.is_pos = 1;
      doc.ignore_pricing_rule = 1;
      doc.company = doc.company || this.pos_profile.company;
      doc.pos_profile = doc.pos_profile || this.pos_profile.name;
      doc.campaign = doc.campaign || this.pos_profile.campaign;
      doc.currency = doc.currency || this.pos_profile.currency;
      doc.naming_series = doc.naming_series || this.pos_profile.naming_series;
      doc.customer = this.customer;
      doc.items = this.get_invoice_items();
      doc.total = this.subtotal;
      doc.discount_amount = flt(this.discount_amount);
      doc.additional_discount_percentage = flt(
        this.additional_discount_percentage
      );
      doc.posa_pos_opening_shift = this.pos_opening_shift.name;
      doc.payments = this.get_payments();
      doc.taxes = [];
      doc.is_return = this.invoice_doc.is_return;
      doc.return_against = this.invoice_doc.return_against;
      doc.posa_offers = this.posa_offers;
      doc.posa_coupons = this.posa_coupons;
      doc.posa_delivery_charges = this.selected_delivery_charge.name;
      doc.posa_delivery_charges_rate = this.delivery_charges_rate || 0;
      doc.posting_date = this.posting_date;
      return doc;
    },

    async get_invoice_from_order_doc() {
      let doc = {};
      if (this.invoice_doc.doctype == "Sales Order") {
        await frappe.call({
          method:
            "posawesome.posawesome.api.posapp.create_sales_invoice_from_order",
          args: {
            sales_order: this.invoice_doc.name,
          },
          // async: false,
          callback: function (r) {
            if (r.message) {
              doc = r.message;
            }
          },
        });
      } else {
        doc = this.invoice_doc;
      }
      const Items = [];
      const updatedItemsData = this.get_invoice_items();
      doc.items.forEach((item) => {
        const updatedData = updatedItemsData.find(
          (updatedItem) => updatedItem.item_code === item.item_code
        );
        if (updatedData) {
          item.item_code = updatedData.item_code;
          item.posa_row_id = updatedData.posa_row_id;
          item.posa_offers = updatedData.posa_offers;
          item.posa_offer_applied = updatedData.posa_offer_applied;
          item.posa_is_offer = updatedData.posa_is_offer;
          item.posa_is_replace = updatedData.posa_is_replace;
          item.is_free_item = updatedData.is_free_item;
          item.qty = flt(updatedData.qty);
          item.rate = flt(updatedData.rate);
          item.uom = updatedData.uom;
          item.amount = flt(updatedData.qty) * flt(updatedData.rate);
          item.conversion_factor = updatedData.conversion_factor;
          item.serial_no = updatedData.serial_no;
          item.discount_percentage = flt(updatedData.discount_percentage);
          item.discount_amount = flt(updatedData.discount_amount);
          item.batch_no = updatedData.batch_no;
          item.posa_notes = updatedData.posa_notes;
          item.posa_delivery_date = updatedData.posa_delivery_date;
          item.price_list_rate = updatedData.price_list_rate;
          Items.push(item);
        }
      });

      doc.items = Items;
      const newItems = [...doc.items];
      const existingItemCodes = new Set(newItems.map((item) => item.item_code));
      updatedItemsData.forEach((updatedItem) => {
        if (!existingItemCodes.has(updatedItem.item_code)) {
          newItems.push(updatedItem);
        }
      });
      doc.items = newItems;
      doc.update_stock = 1;
      doc.is_pos = 1;
      doc.payments = this.get_payments();
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
          qty: flt(item.qty),
          rate: flt(item.rate),
          uom: item.uom,
          amount: flt(item.qty) * flt(item.rate),
          conversion_factor: item.conversion_factor,
          serial_no: item.serial_no,
          discount_percentage: flt(item.discount_percentage),
          discount_amount: flt(item.discount_amount),
          batch_no: item.batch_no,
          posa_notes: item.posa_notes,
          posa_delivery_date: item.posa_delivery_date,
          price_list_rate: item.price_list_rate,
        };
        items_list.push(new_item);
      });

      return items_list;
    },

    get_order_items() {
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
          qty: flt(item.qty),
          rate: flt(item.rate),
          uom: item.uom,
          amount: flt(item.qty) * flt(item.rate),
          conversion_factor: item.conversion_factor,
          serial_no: item.serial_no,
          discount_percentage: flt(item.discount_percentage),
          discount_amount: flt(item.discount_amount),
          batch_no: item.batch_no,
          posa_notes: item.posa_notes,
          posa_delivery_date: item.posa_delivery_date,
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
          account: "",
        });
      });
      return payments;
    },

    update_invoice(doc) {
      var vm = this;
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

    update_invoice_from_order(doc) {
      var vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.update_invoice_from_order",
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

    process_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name) {
        return this.update_invoice(doc);
      } else {
        return this.update_invoice(doc);
      }
    },

    async process_invoice_from_order() {
      const doc = await this.get_invoice_from_order_doc();
      var up_invoice;
      if (doc.name) {
        up_invoice = await this.update_invoice_from_order(doc);
        return up_invoice;
      } else {
        return this.update_invoice_from_order(doc);
      }
    },

    async show_payment() {
      if (!this.customer) {
        this.eventBus.emit("show_message", {
          title: __(`Select a customer`),
          color: "error",
        });
        return;
      }
      if (!this.items.length) {
        this.eventBus.emit("show_message", {
          title: __(`Select items to sell`),
          color: "error",
        });
        return;
      }
      if (!this.validate()) {
        return;
      }
      if (this.invoice_doc.doctype == "Sales Order") {
        this.eventBus.emit("show_payment", "true");
        const invoice_doc = await this.process_invoice_from_order();
        this.eventBus.emit("send_invoice_doc_payment", invoice_doc);
      } else if (this.invoice_doc.doctype == "Sales Invoice") {
        const sales_invoice_item = this.invoice_doc.items[0];
        var sales_invoice_item_doc = {};
        frappe.call({
          method:
            "posawesome.posawesome.api.posapp.get_sales_invoice_child_table",
          args: {
            sales_invoice: this.invoice_doc.name,
            sales_invoice_item: sales_invoice_item.name,
          },
          async: false,
          callback: function (r) {
            if (r.message) {
              sales_invoice_item_doc = r.message;
            }
          },
        });
        if (sales_invoice_item_doc.sales_order) {
          this.eventBus.emit("show_payment", "true");
          const invoice_doc = await this.process_invoice_from_order();
          this.eventBus.emit("send_invoice_doc_payment", invoice_doc);
        } else {
          this.eventBus.emit("show_payment", "true");
          const invoice_doc = this.process_invoice();
          this.eventBus.emit("send_invoice_doc_payment", invoice_doc);
        }
      } else {
        this.eventBus.emit("show_payment", "true");
        const invoice_doc = this.process_invoice();
        this.eventBus.emit("send_invoice_doc_payment", invoice_doc);
      }
    },

    validate() {
      let value = true;
      var vm = this;
      this.items.forEach((item) => {
        if (
          this.pos_profile.posa_max_discount_allowed &&
          !item.posa_offer_applied
        ) {
          if (item.discount_amount && this.flt(item.discount_amount) > 0) {
            // calc discount percentage
            const discount_percentage =
              (this.flt(item.discount_amount) * 100) /
              this.flt(item.price_list_rate);
            if (
              discount_percentage > this.pos_profile.posa_max_discount_allowed
            ) {
              vm.eventBus.emit("show_message", {
                title: __(
                  `Discount percentage for item '{0}' cannot be greater than {1}%`,
                  [item.item_name, this.pos_profile.posa_max_discount_allowed]
                ),
                color: "error",
              });
              value = false;
            }
          }
        }
        if (this.stock_settings.allow_negative_stock != 1) {
          if (
            this.invoiceType == "Invoice" &&
            ((item.is_stock_item && item.stock_qty && !item.actual_qty) ||
              (item.is_stock_item && item.stock_qty > item.actual_qty))
          ) {
            vm.eventBus.emit("show_message", {
              title: __(
                `The existing quantity '{0}' for item '{1}' is not enough`,
                [item.actual_qty, item.item_name]
              ),
              color: "error",
            });
            value = false;
          }
        }
        if (item.qty == 0) {
          vm.eventBus.emit("show_message", {
            title: __(`Quantity for item '{0}' cannot be Zero (0)`, [
              item.item_name,
            ]),
            color: "error",
          });
          value = false;
        }
        if (
          item.max_discount > 0 &&
          item.discount_percentage > item.max_discount
        ) {
          vm.eventBus.emit("show_message", {
            title: __(`Maximum discount for Item {0} is {1}%`, [
              item.item_name,
              item.max_discount,
            ]),
            color: "error",
          });
          value = false;
        }
        if (item.has_serial_no) {
          if (
            !this.invoice_doc.is_return &&
            (!item.serial_no_selected ||
              item.stock_qty != item.serial_no_selected.length)
          ) {
            vm.eventBus.emit("show_message", {
              title: __(`Selected serial numbers of item {0} is incorrect`, [
                item.item_name,
              ]),
              color: "error",
            });
            value = false;
          }
        }
        if (item.has_batch_no) {
          if (item.stock_qty > item.actual_batch_qty) {
            vm.eventBus.emit("show_message", {
              title: __(
                `The existing batch quantity of item {0} is not enough`,
                [item.item_name]
              ),
              color: "error",
            });
            value = false;
          }
        }
        if (this.pos_profile.posa_allow_user_to_edit_additional_discount) {
          const clac_percentage = (this.discount_amount / this.Total) * 100;
          if (clac_percentage > this.pos_profile.posa_max_discount_allowed) {
            vm.eventBus.emit("show_message", {
              title: __(`The discount should not be higher than {0}%`, [
                this.pos_profile.posa_max_discount_allowed,
              ]),
              color: "error",
            });
            value = false;
          }
        }
        if (this.invoice_doc.is_return) {
          if (this.subtotal >= 0) {
            vm.eventBus.emit("show_message", {
              title: __(`Return Invoice Total Not Correct`),
              color: "error",
            });
            value = false;
            return value;
          }
          if (Math.abs(this.subtotal) > Math.abs(this.return_doc.total)) {
            vm.eventBus.emit("show_message", {
              title: __(`Return Invoice Total should not be higher than {0}`, [
                this.return_doc.total,
              ]),
              color: "error",
            });
            value = false;
            return value;
          }
          this.items.forEach((item) => {
            const return_item = this.return_doc.items.find(
              (element) => element.item_code == item.item_code
            );

            if (!return_item) {
              vm.eventBus.emit("show_message", {
                title: __(
                  `The item {0} cannot be returned because it is not in the invoice {1}`,
                  [item.item_name, this.return_doc.name]
                ),
                color: "error",
              });
              value = false;
              return value;
            } else if (
              Math.abs(item.qty) > Math.abs(return_item.qty) ||
              Math.abs(item.qty) == 0
            ) {
              vm.eventBus.emit("show_message", {
                title: __(`The QTY of the item {0} cannot be greater than {1}`, [
                  item.item_name,
                  return_item.qty,
                ]),
                color: "error",
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
      var vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_draft_invoices",
        args: {
          pos_opening_shift: this.pos_opening_shift.name,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            vm.eventBus.emit("open_drafts", r.message);
          }
        },
      });
    },

    get_draft_orders() {
      var vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.search_orders",
        args: {
          company: this.pos_profile.company,
          currency: this.pos_profile.currency,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            vm.eventBus.emit("open_orders", r.message);
          }
        },
      });
    },

    open_returns() {
      this.eventBus.emit("open_returns", this.pos_profile.company);
    },

    close_payments() {
      this.eventBus.emit("show_payment", "false");
    },

    update_items_details(items) {
      if (!items.length > 0) {
        return;
      }
      var vm = this;
      if (!vm.pos_profile) return;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_items_details",
        async: false,
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
      if (!item.item_code || this.invoice_doc.is_return) {
        return;
      }
      var vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_item_detail",
        args: {
          warehouse: this.pos_profile.warehouse,
          doc: this.get_invoice_doc(),
          price_list: this.pos_profile.price_list,
          item: {
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
            uom: item.uom,
            tax_category: "",
            transaction_type: "selling",
            update_stock: this.pos_profile.update_stock,
            price_list: this.get_price_list(),
            has_batch_no: item.has_batch_no,
            serial_no: item.serial_no,
            batch_no: item.batch_no,
            is_stock_item: item.is_stock_item,
          },
        },
        callback: function (r) {
          if (r.message) {
            const data = r.message;
            if (data.batch_no_data) {
              item.batch_no_data = data.batch_no_data;
            }
            if (
              item.has_batch_no &&
              vm.pos_profile.posa_auto_set_batch &&
              !item.batch_no &&
              data.batch_no_data
            ) {
              item.batch_no_data = data.batch_no_data;
              vm.set_batch_qty(item, item.batch_no, false);
            }
            if (data.has_pricing_rule) {
            } else if (
              vm.pos_profile.posa_apply_customer_discount &&
              vm.customer_info.posa_discount > 0 &&
              vm.customer_info.posa_discount <= 100
            ) {
              if (
                item.posa_is_offer == 0 &&
                !item.posa_is_replace &&
                item.posa_offer_applied == 0
              ) {
                if (item.max_discount > 0) {
                  item.discount_percentage =
                    item.max_discount < vm.customer_info.posa_discount
                      ? item.max_discount
                      : vm.customer_info.posa_discount;
                } else {
                  item.discount_percentage = vm.customer_info.posa_discount;
                }
              }
            }
            if (!item.batch_price) {
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

    fetch_customer_details() {
      var vm = this;
      if (this.customer) {
        frappe.call({
          method: "posawesome.posawesome.api.posapp.get_customer_info",
          args: {
            customer: vm.customer,
          },
          async: false,
          callback: (r) => {
            const message = r.message;
            if (!r.exc) {
              vm.customer_info = {
                ...message,
              };
            }
            vm.update_price_list();
          },
        });
      }
    },

    get_price_list() {
      let price_list = this.pos_profile.selling_price_list;
      if (this.customer_info && this.pos_profile) {
        const { customer_price_list, customer_group_price_list } =
          this.customer_info;
        const pos_price_list = this.pos_profile.selling_price_list;
        if (customer_price_list && customer_price_list != pos_price_list) {
          price_list = customer_price_list;
        } else if (
          customer_group_price_list &&
          customer_group_price_list != pos_price_list
        ) {
          price_list = customer_group_price_list;
        }
      }
      return price_list;
    },

    update_price_list() {
      let price_list = this.get_price_list();
      if (price_list == this.pos_profile.selling_price_list) {
        price_list = null;
      }
      this.eventBus.emit("update_customer_price_list", price_list);
    },
    update_discount_umount() {
      const value = flt(this.additional_discount_percentage);
      if (value >= -100 && value <= 100) {
        this.discount_amount = (this.Total * value) / 100;
      } else {
        this.additional_discount_percentage = 0;
        this.discount_amount = 0;
      }
    },

    calc_prices(item, value, $event) {
      if (event.target.id === "rate") {
        item.discount_percentage = 0;
        if (value < item.price_list_rate) {
          item.discount_amount = this.flt(
            this.flt(item.price_list_rate) - flt(value),
            this.currency_precision
          );
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
          item.rate = this.flt(
            flt(item.price_list_rate) -
            (flt(item.price_list_rate) * flt(value)) / 100,
            this.currency_precision
          );
          item.discount_amount = this.flt(
            flt(item.price_list_rate) - flt(+item.rate),
            this.currency_precision
          );
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
        item.discount_amount = this.flt(
          flt(item.price_list_rate) - flt(item.rate),
          this.currency_precision
        );
      } else if (item.discount_amount) {
        item.rate = this.flt(
          flt(item.price_list_rate) - flt(item.discount_amount),
          this.currency_precision
        );
      }
    },

    calc_uom(item, value) {
      const new_uom = item.item_uoms.find((element) => element.uom == value);
      item.conversion_factor = new_uom.conversion_factor;
      if (!item.posa_offer_applied) {
        item.discount_amount = 0;
        item.discount_percentage = 0;
      }
      if (item.batch_price) {
        item.price_list_rate = item.batch_price * new_uom.conversion_factor;
      }
      this.update_item_detail(item);
    },

    calc_stock_qty(item, value) {
      item.stock_qty = item.conversion_factor * value;
    },

    set_serial_no(item) {
      console.log(item)
      if (!item.has_serial_no) return;
      item.serial_no = "";
      item.serial_no_selected.forEach((element) => {
        item.serial_no += element + "\n";
      });
      item.serial_no_selected_count = item.serial_no_selected.length;
      if (item.serial_no_selected_count != item.stock_qty) {
        item.qty = item.serial_no_selected_count;
        this.calc_stock_qty(item, item.qty);
        this.$forceUpdate();
      }
    },

    set_batch_qty(item, value, update = true) {
      console.log(item, value)
      const existing_items = this.items.filter(
        (element) =>
          element.item_code == item.item_code &&
          element.posa_row_id != item.posa_row_id
      );
      const used_batches = {};
      item.batch_no_data.forEach((batch) => {
        used_batches[batch.batch_no] = {
          ...batch,
          used_qty: 0,
          remaining_qty: batch.batch_qty,
        };
        existing_items.forEach((element) => {
          if (element.batch_no && element.batch_no == batch.batch_no) {
            used_batches[batch.batch_no].used_qty += element.qty;
            used_batches[batch.batch_no].remaining_qty -= element.qty;
            used_batches[batch.batch_no].batch_qty -= element.qty;
          }
        });
      });

      // set item batch_no based on:
      // 1. if batch has expiry_date we should use the batch with the nearest expiry_date
      // 2. if batch has no expiry_date we should use the batch with the earliest manufacturing_date
      // 3. we should not use batch with remaining_qty = 0
      // 4. we should the highest remaining_qty
      const batch_no_data = Object.values(used_batches)
        .filter((batch) => batch.remaining_qty > 0)
        .sort((a, b) => {
          if (a.expiry_date && b.expiry_date) {
            return a.expiry_date - b.expiry_date;
          } else if (a.expiry_date) {
            return -1;
          } else if (b.expiry_date) {
            return 1;
          } else if (a.manufacturing_date && b.manufacturing_date) {
            return a.manufacturing_date - b.manufacturing_date;
          } else if (a.manufacturing_date) {
            return -1;
          } else if (b.manufacturing_date) {
            return 1;
          } else {
            return b.remaining_qty - a.remaining_qty;
          }
        });
      if (batch_no_data.length > 0) {
        let batch_to_use = null;
        if (value) {
          batch_to_use = batch_no_data.find((batch) => batch.batch_no == value);
        }
        if (!batch_to_use) {
          batch_to_use = batch_no_data[0];
        }
        item.batch_no = batch_to_use.batch_no;
        item.actual_batch_qty = batch_to_use.batch_qty;
        item.batch_no_expiry_date = batch_to_use.expiry_date;
        if (batch_to_use.batch_price) {
          item.batch_price = batch_to_use.batch_price;
          item.price_list_rate = batch_to_use.batch_price;
          item.rate = batch_to_use.batch_price;
        } else if (update) {
          item.batch_price = null;
          this.update_item_detail(item);
        }
      } else {
        item.batch_no = null;
        item.actual_batch_qty = null;
        item.batch_no_expiry_date = null;
        item.batch_price = null;
      }
      // update item batch_no_data from batch_no_data
      item.batch_no_data = batch_no_data;
    },

    shortOpenPayment(e) {
      if (e.key === "s" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.show_payment();
      }
    },

    shortDeleteFirstItem(e) {
      if (e.key === "d" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.remove_item(this.items[0]);
      }
    },

    shortOpenFirstItem(e) {
      if (e.key === "a" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.expanded = [];
        this.expanded.push(this.items[0]);
      }
    },

    shortSelectDiscount(e) {
      if (e.key === "z" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.$refs.discount.focus();
      }
    },

    makeid(length) {
      let result = "";
      const characters = "abcdefghijklmnopqrstuvwxyz0123456789";
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
      const offers = [];
      this.posOffers.forEach((offer) => {
        if (offer.apply_on === "Item Code") {
          const itemOffer = this.getItemOffer(offer);
          if (itemOffer) {
            offers.push(itemOffer);
          }
        } else if (offer.apply_on === "Item Group") {
          const groupOffer = this.getGroupOffer(offer);
          if (groupOffer) {
            offers.push(groupOffer);
          }
        } else if (offer.apply_on === "Brand") {
          const brandOffer = this.getBrandOffer(offer);
          if (brandOffer) {
            offers.push(brandOffer);
          }
        } else if (offer.apply_on === "Transaction") {
          const transactionOffer = this.getTransactionOffer(offer);
          if (transactionOffer) {
            offers.push(transactionOffer);
          }
        }
      });

      this.setItemGiveOffer(offers);
      this.updatePosOffers(offers);
    },

    setItemGiveOffer(offers) {
      // Set item give offer for replace
      offers.forEach((offer) => {
        if (
          offer.apply_on == "Item Code" &&
          offer.apply_type == "Item Code" &&
          offer.replace_item
        ) {
          offer.give_item = offer.item;
          offer.apply_item_code = offer.item;
        } else if (
          offer.apply_on == "Item Group" &&
          offer.apply_type == "Item Group" &&
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
      if (typeof offer.items === "string") {
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

    checkOfferCoupon(offer) {
      if (offer.coupon_based) {
        const coupon = this.posa_coupons.find(
          (el) => offer.name == el.pos_offer
        );
        if (coupon) {
          offer.coupon = coupon.coupon;
          return true;
        } else {
          return false;
        }
      } else {
        offer.coupon = null;
        return true;
      }
    },

    getItemOffer(offer) {
      let apply_offer = null;
      if (offer.apply_on === "Item Code") {
        if (this.checkOfferCoupon(offer)) {
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.item_code === offer.item) {
              const items = [];
              if (
                offer.offer === "Item Price" &&
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
                  apply_offer = offer;
                }
              }
            }
          });
        }
      }
      return apply_offer;
    },

    getGroupOffer(offer) {
      let apply_offer = null;
      if (offer.apply_on === "Item Group") {
        if (this.checkOfferCoupon(offer)) {
          const items = [];
          let total_count = 0;
          let total_amount = 0;
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.item_group === offer.item_group) {
              if (
                offer.offer === "Item Price" &&
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
              apply_offer = offer;
            }
          }
        }
      }
      return apply_offer;
    },

    getBrandOffer(offer) {
      let apply_offer = null;
      if (offer.apply_on === "Brand") {
        if (this.checkOfferCoupon(offer)) {
          const items = [];
          let total_count = 0;
          let total_amount = 0;
          this.items.forEach((item) => {
            if (!item.posa_is_offer && item.brand === offer.brand) {
              if (
                offer.offer === "Item Price" &&
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
              apply_offer = offer;
            }
          }
        }
      }
      return apply_offer;
    },
    getTransactionOffer(offer) {
      let apply_offer = null;
      if (offer.apply_on === "Transaction") {
        if (this.checkOfferCoupon(offer)) {
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
              apply_offer = offer;
            }
          }
        }
      }
      return apply_offer;
    },

    updatePosOffers(offers) {
      this.eventBus.emit("update_pos_offers", offers);
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
            existOffer.offer === "Give Product" &&
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
            existOffer.offer === "Give Product" &&
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
          } else if (existOffer.offer === "Item Price") {
            this.ApplyOnPrice(offer);
          } else if (existOffer.offer === "Grand Total") {
            this.ApplyOnTotal(offer);
          }
          this.addOfferToItems(existOffer);
        } else {
          this.applyNewOffer(offer);
        }
      });
    },

    removeApplyOffer(invoiceOffer) {
      if (invoiceOffer.offer === "Item Price") {
        this.RemoveOnPrice(invoiceOffer);
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      if (invoiceOffer.offer === "Give Product") {
        const item_to_remove = this.items.find(
          (item) => item.posa_row_id == invoiceOffer.give_item_row_id
        );
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
        this.remove_item(item_to_remove);
      }
      if (invoiceOffer.offer === "Grand Total") {
        this.RemoveOnTotal(invoiceOffer);
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      if (invoiceOffer.offer === "Loyalty Point") {
        const index = this.posa_offers.findIndex(
          (el) => el.row_id === invoiceOffer.row_id
        );
        this.posa_offers.splice(index, 1);
      }
      this.deleteOfferFromItems(invoiceOffer);
    },

    applyNewOffer(offer) {
      if (offer.offer === "Item Price") {
        this.ApplyOnPrice(offer);
      }
      if (offer.offer === "Give Product") {
        let itemsRowID;
        if (typeof offer.items === "string") {
          itemsRowID = JSON.parse(offer.items);
        } else {
          itemsRowID = offer.items;
        }
        if (
          offer.apply_on == "Item Code" &&
          offer.apply_type == "Item Code" &&
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
          offer.apply_on == "Item Group" &&
          offer.apply_type == "Item Group" &&
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
      if (offer.offer === "Grand Total") {
        this.ApplyOnTotal(offer);
      }
      if (offer.offer === "Loyalty Point") {
        this.eventBus.emit("show_message", {
          title: __("Loyalty Point Offer Applied"),
          color: "success",
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
        coupon_based: offer.coupon_based,
        coupon: offer.coupon,
      };
      this.posa_offers.push(newOffer);
      this.addOfferToItems(newOffer);
    },

    ApplyOnGiveProduct(offer, item_code) {
      if (!item_code) {
        item_code = offer.give_item;
      }
      const items = this.allItems;
      const item = items.find((item) => item.item_code == item_code);
      if (!item) {
        return;
      }
      const new_item = { ...item };
      new_item.qty = offer.given_qty;
      new_item.stock_qty = offer.given_qty;
      new_item.rate = offer.discount_type === "Rate" ? offer.rate : item.rate;
      new_item.discount_amount =
        offer.discount_type === "Discount Amount" ? offer.discount_amount : 0;
      new_item.discount_percentage =
        offer.discount_type === "Discount Percentage"
          ? offer.discount_percentage
          : 0;
      new_item.discount_amount_per_item = 0;
      new_item.uom = item.uom ? item.uom : item.stock_uom;
      new_item.actual_batch_qty = "";
      new_item.conversion_factor = 1;
      new_item.posa_offers = JSON.stringify([]);
      new_item.posa_offer_applied = 0;
      new_item.posa_is_offer = 1;
      new_item.posa_is_replace = null;
      new_item.posa_notes = "";
      new_item.posa_delivery_date = "";
      new_item.is_free_item =
        (offer.discount_type === "Rate" && !offer.rate) ||
          (offer.discount_type === "Discount Percentage" &&
            offer.discount_percentage == 0)
          ? 1
          : 0;
      new_item.posa_row_id = this.makeid(20);
      new_item.price_list_rate =
        (offer.discount_type === "Rate" && !offer.rate) ||
          (offer.discount_type === "Discount Percentage" &&
            offer.discount_percentage == 0)
          ? 0
          : item.rate;
      if (
        (!this.pos_profile.posa_auto_set_batch && new_item.has_batch_no) ||
        new_item.has_serial_no
      ) {
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
            if (offer.discount_type === "Rate") {
              item.rate = offer.rate;
            } else if (offer.discount_type === "Discount Percentage") {
              item.discount_percentage += offer.discount_percentage;
            } else if (offer.discount_type === "Discount Amount") {
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
            if (originalOffer.discount_type === "Rate") {
              item.rate = item.price_list_rate;
            } else if (originalOffer.discount_type === "Discount Percentage") {
              item.discount_percentage -= offer.discount_percentage;
              if (!item.discount_percentage) {
                item.discount_percentage = 0;
                item.discount_amount = 0;
                item.rate = item.price_list_rate;
              }
            } else if (originalOffer.discount_type === "Discount Amount") {
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
        this.discount_amount = this.flt(
          (flt(this.Total) * flt(offer.discount_percentage)) / 100,
          this.currency_precision
        );
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
              if (offer.offer === "Item Price") {
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
            if (offer.offer === "Item Price") {
              exist_item.posa_offer_applied = 0;
            }
            exist_item.posa_offers = JSON.stringify(updated_item_offers);
          }
        });
      });
    },

    validate_due_date(item) {
      const today = frappe.datetime.now_date();
      const parse_today = Date.parse(today);
      const new_date = Date.parse(item.posa_delivery_date);
      if (new_date < parse_today) {
        setTimeout(() => {
          item.posa_delivery_date = today;
        }, 0);
      }
    },
    load_print_page(invoice_name) {
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        "/printview?doctype=Sales%20Invoice&name=" +
        invoice_name +
        "&trigger_print=1" +
        "&format=" +
        print_format +
        "&no_letterhead=" +
        letter_head;
      const printWindow = window.open(url, "Print");
      printWindow.addEventListener(
        "load",
        function () {
          printWindow.print();
          // printWindow.close();
          // NOTE : uncomoent this to auto closing printing window
        },
        true
      );
    },

    print_draft_invoice() {
      if (!this.pos_profile.posa_allow_print_draft_invoices) {
        this.eventBus.emit("show_message", {
          title: __(`You are not allowed to print draft invoices`),
          color: "error",
        });
        return;
      }
      let invoice_name = this.invoice_doc.name;
      frappe.run_serially([
        () => {
          const invoice_doc = this.save_and_clear_invoice();
          invoice_name = invoice_doc.name ? invoice_doc.name : invoice_name;
        },
        () => {
          this.load_print_page(invoice_name);
        },
      ]);
    },
    set_delivery_charges() {
      var vm = this;
      if (
        !this.pos_profile ||
        !this.customer ||
        !this.pos_profile.posa_use_delivery_charges
      ) {
        this.delivery_charges = [];
        this.delivery_charges_rate = 0;
        this.selected_delivery_charge = "";
        return;
      }
      this.delivery_charges_rate = 0;
      this.selected_delivery_charge = "";
      frappe.call({
        method:
          "posawesome.posawesome.api.posapp.get_applicable_delivery_charges",
        args: {
          company: this.pos_profile.company,
          pos_profile: this.pos_profile.name,
          customer: this.customer,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            if (r.message?.length) {
              console.log(r.message)
              vm.delivery_charges = r.message;
            }
          }
        },
      });
    },
    deliveryChargesFilter(itemText, queryText, itemRow) {
      const item = itemRow.raw;
      console.log("dl charges", item)
      const textOne = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();
      return textOne.indexOf(searchText) > -1;
    },
    update_delivery_charges() {
 
      if (this.selected_delivery_charge) {
        this.delivery_charges_rate = this.selected_delivery_charge.rate;
      } else {
        this.delivery_charges_rate = 0;
      }
    },
  },

  mounted() {
    this.eventBus.on("register_pos_profile", (data) => {
      this.pos_profile = data.pos_profile;
      this.customer = data.pos_profile.customer;
      this.pos_opening_shift = data.pos_opening_shift;
      this.stock_settings = data.stock_settings;
      this.float_precision =
        frappe.defaults.get_default("float_precision") || 2;
      this.currency_precision =
        frappe.defaults.get_default("currency_precision") || 2;
      this.invoiceType = this.pos_profile.posa_default_sales_order
        ? "Order"
        : "Invoice";
    });
    this.eventBus.on("add_item", (item) => {
      this.add_item(item);
    });
    this.eventBus.on("update_customer", (customer) => {
      this.customer = customer;
    });
    this.eventBus.on("fetch_customer_details", () => {
      this.fetch_customer_details();
    });
    this.eventBus.on("clear_invoice", () => {
      this.clear_invoice();
    });
    this.eventBus.on("load_invoice", (data) => {
      this.load_invoice(data);
    });
    this.eventBus.on("load_order", (data) => {
      this.new_order(data);
      // this.eventBus.emit("set_pos_coupons", data.posa_coupons);
    });
    this.eventBus.on("set_offers", (data) => {
      this.posOffers = data;
    });
    this.eventBus.on("update_invoice_offers", (data) => {
      this.updateInvoiceOffers(data);
    });
    this.eventBus.on("update_invoice_coupons", (data) => {
      this.posa_coupons = data;
      this.handelOffers();
    });
    this.eventBus.on("set_all_items", (data) => {
      this.allItems = data;
      this.items.forEach((item) => {
        this.update_item_detail(item);
      });
    });
    this.eventBus.on("load_return_invoice", (data) => {
      this.load_invoice(data.invoice_doc);
      this.discount_amount = -data.return_doc.discount_amount;
      this.additional_discount_percentage =
        -data.return_doc.additional_discount_percentage;
      this.return_doc = data.return_doc;
    });
    this.eventBus.on("set_new_line", (data) => {
      this.new_line = data;
    });
  },
  beforeUnmount() {
    evntBus.$off("register_pos_profile");
    evntBus.$off("add_item");
    evntBus.$off("update_customer");
    evntBus.$off("fetch_customer_details");
    evntBus.$off("clear_invoice");
    evntBus.$off("set_offers");
    evntBus.$off("update_invoice_offers");
    evntBus.$off("update_invoice_coupons");
    evntBus.$off("set_all_items");
  },
  created() {
    document.addEventListener("keydown", this.shortOpenPayment.bind(this));
    document.addEventListener("keydown", this.shortDeleteFirstItem.bind(this));
    document.addEventListener("keydown", this.shortOpenFirstItem.bind(this));
    document.addEventListener("keydown", this.shortSelectDiscount.bind(this));
  },
  unmounted() {
    document.removeEventListener("keydown", this.shortOpenPayment);
    document.removeEventListener("keydown", this.shortDeleteFirstItem);
    document.removeEventListener("keydown", this.shortOpenFirstItem);
    document.removeEventListener("keydown", this.shortSelectDiscount);
  },
  watch: {
    customer() {
      this.close_payments();
      this.eventBus.emit("set_customer", this.customer);
      this.fetch_customer_details();
      this.set_delivery_charges();
    },
    customer_info() {
      this.eventBus.emit("set_customer_info_to_edit", this.customer_info);
    },
    expanded(data_value) {
      // this.update_items_details(data_value);
      if (data_value.length > 0) {
        this.update_item_detail(data_value[0]);
      }
    },
    discount_percentage_offer_name() {
      this.eventBus.emit("update_discount_percentage_offer_name", {
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
    invoiceType() {
      this.eventBus.emit("update_invoice_type", this.invoiceType);
    },
    discount_amount() {
      if (!this.discount_amount || this.discount_amount == 0) {
        this.additional_discount_percentage = 0;
      } else if (this.pos_profile.posa_use_percentage_discount) {
        this.additional_discount_percentage =
          (this.discount_amount / this.Total) * 100;
      } else {
        this.additional_discount_percentage = 0;
      }
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
