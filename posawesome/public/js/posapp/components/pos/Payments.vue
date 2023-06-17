<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5 pa-1"
      style="max-height: 76vh; height: 76vh"
    >
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        top
        color="info"
      ></v-progress-linear>
      <div class="overflow-y-auto px-2 pt-2" style="max-height: 75vh">
        <v-row v-if="invoice_doc" class="px-1 py-0">
          <v-col cols="7">
            <v-text-field
              outlined
              color="primary"
              :label="frappe._('Paid Amount')"
              background-color="white"
              hide-details
              :value="formtCurrency(total_payments)"
              readonly
              :prefix="currencySymbol(invoice_doc.currency)"
              dense
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              outlined
              color="primary"
              :label="frappe._(diff_lable)"
              background-color="white"
              hide-details
              :value="formtCurrency(diff_payment)"
              readonly
              :prefix="currencySymbol(invoice_doc.currency)"
              dense
            ></v-text-field>
          </v-col>

          <v-col cols="7" v-if="diff_payment < 0 && !invoice_doc.is_return">
            <v-text-field
              outlined
              color="primary"
              :label="frappe._('Paid Change')"
              background-color="white"
              v-model="paid_change"
              @input="set_paid_change()"
              :prefix="currencySymbol(invoice_doc.currency)"
              :rules="paid_change_rules"
              dense
              readonly
              type="number"
            ></v-text-field>
          </v-col>

          <v-col cols="5" v-if="diff_payment < 0 && !invoice_doc.is_return">
            <v-text-field
              outlined
              color="primary"
              :label="frappe._('Credit Change')"
              background-color="white"
              hide-details
              :value="formtCurrency(credit_change)"
              readonly
              :prefix="currencySymbol(invoice_doc.currency)"
              dense
            ></v-text-field>
          </v-col>
        </v-row>
        <v-divider></v-divider>

        <div v-if="is_cashback">
          <v-row
            class="pyments px-1 py-0"
            v-for="payment in invoice_doc.payments"
            :key="payment.name"
          >
            <v-col cols="6" v-if="!is_mpesa_c2b_payment(payment)">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._(payment.mode_of_payment)"
                background-color="white"
                hide-details
                :value="formtCurrency(payment.amount)"
                @change="
                  setFormatedCurrency(payment, 'amount', null, true, $event)
                "
                :rules="[isNumber]"
                :prefix="currencySymbol(invoice_doc.currency)"
                @focus="set_rest_amount(payment.idx)"
                :readonly="invoice_doc.is_return ? true : false"
              ></v-text-field>
            </v-col>
            <v-col
              v-if="!is_mpesa_c2b_payment(payment)"
              :cols="
                6
                  ? (payment.type != 'Phone' ||
                      payment.amount == 0 ||
                      !request_payment_field) &&
                    !is_mpesa_c2b_payment(payment)
                  : 3
              "
            >
              <v-btn
                block
                class=""
                color="primary"
                dark
                @click="set_full_amount(payment.idx)"
                >{{ payment.mode_of_payment }}</v-btn
              >
            </v-col>
            <v-col v-if="is_mpesa_c2b_payment(payment)" :cols="12" class="pl-3">
              <v-btn
                block
                class=""
                color="success"
                dark
                @click="mpesa_c2b_dialg(payment)"
              >
                {{ __(`Get Payments ${payment.mode_of_payment}`) }}
              </v-btn>
            </v-col>
            <v-col
              v-if="
                payment.type == 'Phone' &&
                payment.amount > 0 &&
                request_payment_field
              "
              :cols="3"
              class="pl-1"
            >
              <v-btn
                block
                class=""
                color="success"
                dark
                :disabled="payment.amount == 0"
                @click="
                  (phone_dialog = true),
                    (payment.amount = flt(payment.amount, 0))
                "
              >
                {{ __('Request') }}
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <v-row
          class="pyments px-1 py-0"
          v-if="
            invoice_doc &&
            available_pioints_amount > 0 &&
            !invoice_doc.is_return
          "
        >
          <v-col cols="7">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Redeem Loyalty Points')"
              background-color="white"
              hide-details
              v-model="loyalty_amount"
              type="number"
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('You can redeem upto')"
              background-color="white"
              hide-details
              :value="formtFloat(available_pioints_amount)"
              :prefix="currencySymbol(invoice_doc.currency)"
              disabled
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row
          class="pyments px-1 py-0"
          v-if="
            invoice_doc &&
            available_customer_credit > 0 &&
            !invoice_doc.is_return &&
            redeem_customer_credit
          "
        >
          <v-col cols="7">
            <v-text-field
              dense
              outlined
              disabled
              color="primary"
              :label="frappe._('Redeemed Customer Credit')"
              background-color="white"
              hide-details
              v-model="redeemed_customer_credit"
              type="number"
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('You can redeem credit upto')"
              background-color="white"
              hide-details
              :value="formtCurrency(available_customer_credit)"
              :prefix="currencySymbol(invoice_doc.currency)"
              disabled
            ></v-text-field>
          </v-col>
        </v-row>
        <v-divider></v-divider>

        <v-row class="px-1 py-0">
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Net Total')"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.net_total)"
              disabled
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Tax and Charges')"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.total_taxes_and_charges)"
              disabled
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Total Amount')"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.total)"
              disabled
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Discount Amount')"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.discount_amount)"
              disabled
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="primary"
              :label="frappe._('Grand Total')"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.grand_total)"
              disabled
              :prefix="currencySymbol(invoice_doc.currency)"
            ></v-text-field>
          </v-col>
          <v-col
            cols="6"
            v-if="pos_profile.posa_allow_sales_order && invoiceType == 'Order'"
          >
            <v-menu
              ref="order_delivery_date"
              v-model="order_delivery_date"
              :close-on-content-click="false"
              transition="scale-transition"
              dense
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="invoice_doc.posa_delivery_date"
                  :label="frappe._('Delivery Date')"
                  readonly
                  outlined
                  dense
                  background-color="white"
                  clearable
                  color="primary"
                  hide-details
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="invoice_doc.posa_delivery_date"
                no-title
                scrollable
                color="primary"
                :min="frappe.datetime.now_date()"
                @input="order_delivery_date = false"
              >
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" v-if="invoice_doc.posa_delivery_date">
            <v-autocomplete
              dense
              clearable
              auto-select-first
              outlined
              color="primary"
              :label="frappe._('Address')"
              v-model="invoice_doc.shipping_address_name"
              :items="addresses"
              item-text="address_title"
              item-value="name"
              background-color="white"
              no-data-text="Address not found"
              hide-details
              :filter="addressFilter"
              append-icon="mdi-plus"
              @click:append="new_address"
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="primary--text subtitle-1"
                      v-html="data.item.address_title"
                    ></v-list-item-title>
                    <v-list-item-title
                      v-html="data.item.address_line1"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-if="data.item.custoaddress_line2mer_name"
                      v-html="data.item.address_line2"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.city"
                      v-html="data.item.city"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.state"
                      v-html="data.item.state"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.country"
                      v-html="data.item.mobile_no"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.address_type"
                      v-html="data.item.address_type"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" v-if="pos_profile.posa_display_additional_notes">
            <v-textarea
              class="pa-0"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
              auto-grow
              rows="2"
              :label="frappe._('Additional Notes')"
              v-model="invoice_doc.posa_notes"
              :value="invoice_doc.posa_notes"
            ></v-textarea>
          </v-col>
        </v-row>

        <div v-if="pos_profile.posa_allow_customer_purchase_order">
          <v-divider></v-divider>
          <v-row class="px-1 py-0" justify="center" align="start">
            <v-col cols="6">
              <v-text-field
                v-model="invoice_doc.po_no"
                :label="frappe._('Purchase Order')"
                outlined
                dense
                background-color="white"
                clearable
                color="primary"
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-menu
                ref="po_date_menu"
                v-model="po_date_menu"
                :close-on-content-click="false"
                transition="scale-transition"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="invoice_doc.po_date"
                    :label="frappe._('Purchase Order Date')"
                    readonly
                    outlined
                    dense
                    hide-details
                    v-bind="attrs"
                    v-on="on"
                    color="primary"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="invoice_doc.po_date"
                  no-title
                  scrollable
                  color="primary"
                  @input="po_date_menu = false"
                >
                </v-date-picker>
              </v-menu>
            </v-col>
          </v-row>
        </div>
        <v-divider></v-divider>
        <v-row class="px-1 py-0" align="start" no-gutters>
          <v-col
            cols="6"
            v-if="
              pos_profile.posa_allow_write_off_change &&
              diff_payment > 0 &&
              !invoice_doc.is_return
            "
          >
            <v-switch
              class="my-0 py-0"
              v-model="is_write_off_change"
              flat
              :label="frappe._('Write Off Difference Amount')"
            ></v-switch>
          </v-col>
          <v-col
            cols="6"
            v-if="pos_profile.posa_allow_credit_sale && !invoice_doc.is_return"
          >
            <v-switch
              v-model="is_credit_sale"
              flat
              :label="frappe._('Is Credit Sale')"
              class="my-0 py-0"
            ></v-switch>
          </v-col>
          <v-col
            cols="6"
            v-if="invoice_doc.is_return && pos_profile.use_cashback"
          >
            <v-switch
              v-model="is_cashback"
              flat
              :label="frappe._('Is Cashback')"
              class="my-0 py-0"
            ></v-switch>
          </v-col>
          <v-col cols="6" v-if="is_credit_sale">
            <v-menu
              ref="date_menu"
              v-model="date_menu"
              :close-on-content-click="false"
              transition="scale-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="invoice_doc.due_date"
                  :label="frappe._('Due Date')"
                  readonly
                  outlined
                  dense
                  hide-details
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="invoice_doc.due_date"
                no-title
                scrollable
                color="primary"
                :min="frappe.datetime.now_date()"
                @input="date_menu = false"
              >
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col
            cols="6"
            v-if="!invoice_doc.is_return && pos_profile.use_customer_credit"
          >
            <v-switch
              v-model="redeem_customer_credit"
              flat
              :label="frappe._('Use Customer Credit')"
              class="my-0 py-0"
              @change="get_available_credit($event)"
            ></v-switch>
          </v-col>
        </v-row>
        <div
          v-if="
            invoice_doc &&
            available_customer_credit > 0 &&
            !invoice_doc.is_return &&
            redeem_customer_credit
          "
        >
          <v-row v-for="(row, idx) in customer_credit_dict" :key="idx">
            <v-col cols="4">
              <div class="pa-2 py-3">{{ row.credit_origin }}</div>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Available Credit')"
                background-color="white"
                hide-details
                :value="formtCurrency(row.total_credit)"
                disabled
                :prefix="currencySymbol(invoice_doc.currency)"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Redeem Credit')"
                background-color="white"
                hide-details
                type="number"
                v-model="row.credit_to_redeem"
                :prefix="currencySymbol(invoice_doc.currency)"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>
        <v-divider></v-divider>
        <v-row class="pb-0 mb-2" align="start">
          <v-col cols="12">
            <v-autocomplete
              dense
              clearable
              auto-select-first
              outlined
              color="primary"
              :label="frappe._('Sales Person')"
              v-model="sales_person"
              :items="sales_persons"
              item-text="sales_person_name"
              item-value="name"
              background-color="white"
              :no-data-text="__('Sales Person not found')"
              hide-details
              :filter="salesPersonFilter"
              :disabled="readonly"
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="primary--text subtitle-1"
                      v-html="data.item.sales_person_name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-if="data.item.sales_person_name != data.item.name"
                      v-html="`ID: ${data.item.name}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </div>
    </v-card>

    <v-card flat class="cards mb-0 mt-3 py-0">
      <v-row align="start" no-gutters>
        <v-col cols="6">
          <v-btn
            block
            large
            color="primary"
            dark
            @click="submit"
            :disabled="vaildatPayment"
            >{{ __('Submit') }}</v-btn
          >
        </v-col>
        <v-col cols="6" class="pl-1">
          <v-btn
            block
            large
            color="success"
            dark
            @click="submit(undefined, false, true)"
            :disabled="vaildatPayment"
            >{{ __('Submit & Print') }}</v-btn
          >
        </v-col>
        <v-col cols="12">
          <v-btn
            block
            class="mt-2 pa-1"
            large
            color="error"
            dark
            @click="back_to_invoice"
            >{{ __('Cancel Payment') }}</v-btn
          >
        </v-col>
      </v-row>
    </v-card>
    <div>
      <v-dialog v-model="phone_dialog" max-width="400px">
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Confirm Mobile Number')
            }}</span>
          </v-card-title>
          <v-card-text class="pa-0">
            <v-container>
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Mobile Number')"
                background-color="white"
                hide-details
                v-model="invoice_doc.contact_mobile"
                type="number"
              ></v-text-field>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="phone_dialog = false">{{
              __('Close')
            }}</v-btn>
            <v-btn color="primary" dark @click="request_payment">{{
              __('Request')
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import format from '../../format';
export default {
  mixins: [format],
  data: () => ({
    loading: false,
    pos_profile: '',
    invoice_doc: '',
    loyalty_amount: 0,
    is_credit_sale: 0,
    is_write_off_change: 0,
    date_menu: false,
    po_date_menu: false,
    addresses: [],
    sales_persons: [],
    sales_person: '',
    paid_change: 0,
    order_delivery_date: false,
    paid_change_rules: [],
    is_return: false,
    is_cashback: true,
    redeem_customer_credit: false,
    customer_credit_dict: [],
    phone_dialog: false,
    invoiceType: 'Invoice',
    pos_settings: '',
    customer_info: '',
    mpesa_modes: [],
  }),

  methods: {
    back_to_invoice() {
      evntBus.$emit('show_payment', 'false');
      evntBus.$emit('set_customer_readonly', false);
    },
    submit(event, payment_received = false, print = false) {
      if (!this.invoice_doc.is_return && this.total_payments < 0) {
        evntBus.$emit('show_mesage', {
          text: `Payments not correct`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }
      // validate phone payment
      let phone_payment_is_valid = true;
      if (!payment_received) {
        this.invoice_doc.payments.forEach((payment) => {
          if (
            payment.type == 'Phone' &&
            ![0, '0', '', null, undefined].includes(payment.amount)
          ) {
            phone_payment_is_valid = false;
          }
        });
        if (!phone_payment_is_valid) {
          evntBus.$emit('show_mesage', {
            text: __(
              'Please request phone payment or use other payment method'
            ),
            color: 'error',
          });
          frappe.utils.play_sound('error');
          console.error('phone payment not requested');
          return;
        }
      }

      if (
        !this.pos_profile.posa_allow_partial_payment &&
        this.total_payments < this.invoice_doc.grand_total
      ) {
        evntBus.$emit('show_mesage', {
          text: `The amount paid is not complete`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      if (
        this.pos_profile.posa_allow_partial_payment &&
        !this.pos_profile.posa_allow_credit_sale &&
        this.total_payments == 0
      ) {
        evntBus.$emit('show_mesage', {
          text: `Please enter the amount paid`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      if (!this.paid_change) this.paid_change = 0;

      if (this.paid_change > -this.diff_payment) {
        evntBus.$emit('show_mesage', {
          text: `Paid change can not be greater than total change!`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      let total_change = this.flt(
        this.flt(this.paid_change) + this.flt(-this.credit_change)
      );

      if (this.is_cashback && total_change != -this.diff_payment) {
        evntBus.$emit('show_mesage', {
          text: `Error in change calculations!`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      let credit_calc_check = this.customer_credit_dict.filter((row) => {
        if (flt(row.credit_to_redeem))
          return flt(row.credit_to_redeem) > flt(row.total_credit);
        else return false;
      });

      if (credit_calc_check.length > 0) {
        evntBus.$emit('show_mesage', {
          text: `redeamed credit can not greater than its total.`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      if (
        !this.invoice_doc.is_return &&
        this.redeemed_customer_credit > this.invoice_doc.grand_total
      ) {
        evntBus.$emit('show_mesage', {
          text: `can not redeam customer credit more than invoice total`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      this.submit_invoice(print);
      this.customer_credit_dict = [];
      this.redeem_customer_credit = false;
      this.is_cashback = true;
      this.sales_person = '';

      evntBus.$emit('new_invoice', 'false');
      this.back_to_invoice();
    },
    submit_invoice(print) {
      this.invoice_doc.payments.forEach((payment) => {
        payment.amount = flt(payment.amount);
      });
      if (this.customer_credit_dict.length) {
        this.customer_credit_dict.forEach((row) => {
          row.credit_to_redeem = flt(row.credit_to_redeem);
        });
      }
      let data = {};
      data['total_change'] = -this.diff_payment;
      data['paid_change'] = this.paid_change;
      data['credit_change'] = -this.credit_change;
      data['redeemed_customer_credit'] = this.redeemed_customer_credit;
      data['customer_credit_dict'] = this.customer_credit_dict;
      data['is_cashback'] = this.is_cashback;

      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.submit_invoice',
        args: {
          data: data,
          invoice: this.invoice_doc,
        },
        async: true,
        callback: function (r) {
          if (r.message) {
            if (print) {
              vm.load_print_page();
            }
            evntBus.$emit('set_last_invoice', vm.invoice_doc.name);
            evntBus.$emit('show_mesage', {
              text: `Invoice ${r.message.name} is Submited`,
              color: 'success',
            });
            frappe.utils.play_sound('submit');
            this.addresses = [];
          }
        },
      });
    },
    set_full_amount(idx) {
      this.invoice_doc.payments.forEach((payment) => {
        payment.amount = payment.idx == idx ? this.invoice_doc.grand_total : 0;
      });
    },
    set_rest_amount(idx) {
      this.invoice_doc.payments.forEach((payment) => {
        if (
          payment.idx == idx &&
          payment.amount == 0 &&
          this.diff_payment > 0
        ) {
          payment.amount = this.diff_payment;
        }
      });
    },
    clear_all_amounts() {
      this.invoice_doc.payments.forEach((payment) => {
        payment.amount = 0;
      });
    },
    load_print_page() {
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        '/printview?doctype=Sales%20Invoice&name=' +
        this.invoice_doc.name +
        '&trigger_print=1' +
        '&format=' +
        print_format +
        '&no_letterhead=' +
        letter_head;
      const printWindow = window.open(url, 'Print');
      printWindow.addEventListener(
        'load',
        function () {
          printWindow.print();
          // printWindow.close();
          // NOTE : uncomoent this to auto closing printing window
        },
        true
      );
    },
    validate_due_date() {
      const today = frappe.datetime.now_date();
      const parse_today = Date.parse(today);
      const new_date = Date.parse(this.invoice_doc.due_date);
      if (new_date < parse_today) {
        setTimeout(() => {
          this.invoice_doc.due_date = today;
        }, 0);
      }
    },
    shortPay(e) {
      if (e.key === 'x' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.submit();
      }
    },
    set_paid_change() {
      if (!this.paid_change) this.paid_change = 0;

      this.paid_change_rules = [];
      let change = -this.diff_payment;
      if (this.paid_change > change) {
        this.paid_change_rules = [
          'Paid change can not be greater than total change!',
        ];
        this.credit_change = 0;
      }
    },
    get_available_credit(e) {
      this.clear_all_amounts();
      if (e) {
        frappe
          .call('posawesome.posawesome.api.posapp.get_available_credit', {
            customer: this.invoice_doc.customer,
            company: this.pos_profile.company,
          })
          .then((r) => {
            const data = r.message;
            if (data.length) {
              this.customer_credit_dict = data;
            } else {
              this.customer_credit_dict = [];
            }
          });
      } else {
        this.customer_credit_dict = [];
      }
    },
    get_addresses() {
      const vm = this;
      if (!vm.invoice_doc) {
        return;
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_addresses',
        args: { customer: vm.invoice_doc.customer },
        async: true,
        callback: function (r) {
          if (!r.exc) {
            vm.addresses = r.message;
          } else {
            vm.addresses = [];
          }
        },
      });
    },
    addressFilter(item, queryText, itemText) {
      const textOne = item.address_title
        ? item.address_title.toLowerCase()
        : '';
      const textTwo = item.address_line1
        ? item.address_line1.toLowerCase()
        : '';
      const textThree = item.address_line2
        ? item.address_line2.toLowerCase()
        : '';
      const textFour = item.city ? item.city.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();
      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
    new_address() {
      evntBus.$emit('open_new_address', this.invoice_doc.customer);
    },
    get_sales_person_names() {
      const vm = this;
      if (
        vm.pos_profile.posa_local_storage &&
        localStorage.sales_persons_storage
      ) {
        vm.sales_persons = JSON.parse(
          localStorage.getItem('sales_persons_storage')
        );
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_sales_person_names',
        callback: function (r) {
          if (r.message) {
            vm.sales_persons = r.message;
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('sales_persons_storage', '');
              localStorage.setItem(
                'sales_persons_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    salesPersonFilter(item, queryText, itemText) {
      const textOne = item.sales_person_name
        ? item.sales_person_name.toLowerCase()
        : '';
      const textTwo = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1
      );
    },
    request_payment() {
      this.phone_dialog = false;
      const vm = this;
      if (!this.invoice_doc.contact_mobile) {
        evntBus.$emit('show_mesage', {
          text: __(`Pleas Set Customer Mobile Number`),
          color: 'error',
        });
        evntBus.$emit('open_edit_customer');
        this.back_to_invoice();
        return;
      }
      evntBus.$emit('freeze', {
        title: __(`Waiting for payment... `),
      });
      this.invoice_doc.payments.forEach((payment) => {
        payment.amount = flt(payment.amount);
      });
      let formData = { ...this.invoice_doc };
      formData['total_change'] = -this.diff_payment;
      formData['paid_change'] = this.paid_change;
      formData['credit_change'] = -this.credit_change;
      formData['redeemed_customer_credit'] = this.redeemed_customer_credit;
      formData['customer_credit_dict'] = this.customer_credit_dict;
      formData['is_cashback'] = this.is_cashback;

      frappe
        .call({
          method: 'posawesome.posawesome.api.posapp.update_invoice',
          args: {
            data: formData,
          },
          async: false,
          callback: function (r) {
            if (r.message) {
              vm.invoice_doc = r.message;
            }
          },
        })
        .then(() => {
          frappe
            .call({
              method: 'posawesome.posawesome.api.posapp.create_payment_request',
              args: {
                doc: vm.invoice_doc,
              },
            })
            .fail(() => {
              evntBus.$emit('unfreeze');
              evntBus.$emit('show_mesage', {
                text: __(`Payment request failed`),
                color: 'error',
              });
            })
            .then(({ message }) => {
              const payment_request_name = message.name;
              setTimeout(() => {
                frappe.db
                  .get_value('Payment Request', payment_request_name, [
                    'status',
                    'grand_total',
                  ])
                  .then(({ message }) => {
                    if (message.status != 'Paid') {
                      evntBus.$emit('unfreeze');
                      evntBus.$emit('show_mesage', {
                        text: __(
                          `Payment Request took too long to respond. Please try requesting for payment again`
                        ),
                        color: 'error',
                      });
                    } else {
                      evntBus.$emit('unfreeze');
                      evntBus.$emit('show_mesage', {
                        text: __('Payment of {0} received successfully.', [
                          vm.formtCurrency(
                            message.grand_total,
                            vm.invoice_doc.currency,
                            0
                          ),
                        ]),
                        color: 'success',
                      });
                      frappe.db
                        .get_doc('Sales Invoice', vm.invoice_doc.name)
                        .then((doc) => {
                          vm.invoice_doc = doc;
                          vm.submit(null, true);
                        });
                    }
                  });
              }, 30000);
            });
        });
    },
    get_mpesa_modes() {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.m_pesa.get_mpesa_mode_of_payment',
        args: { company: vm.pos_profile.company },
        async: true,
        callback: function (r) {
          if (!r.exc) {
            vm.mpesa_modes = r.message;
          } else {
            vm.mpesa_modes = [];
          }
        },
      });
    },
    is_mpesa_c2b_payment(payment) {
      if (
        this.mpesa_modes.includes(payment.mode_of_payment) &&
        payment.type == 'Bank'
      ) {
        payment.amount = 0;
        return true;
      } else {
        return false;
      }
    },
    mpesa_c2b_dialg(payment) {
      const data = {
        company: this.pos_profile.company,
        mode_of_payment: payment.mode_of_payment,
        customer: this.invoice_doc.customer,
      };
      evntBus.$emit('open_mpesa_payments', data);
    },
    set_mpesa_payment(payment) {
      this.pos_profile.use_customer_credit = 1;
      this.redeem_customer_credit = true;
      const advance = {
        type: 'Advance',
        credit_origin: payment.name,
        total_credit: flt(payment.unallocated_amount),
        credit_to_redeem: flt(payment.unallocated_amount),
      };
      this.clear_all_amounts();
      this.customer_credit_dict.push(advance);
    },
  },

  computed: {
    total_payments() {
      let total = parseFloat(this.invoice_doc.loyalty_amount);
      if (this.invoice_doc && this.invoice_doc.payments) {
        this.invoice_doc.payments.forEach((payment) => {
          total += this.flt(payment.amount);
        });
      }

      total += this.flt(this.redeemed_customer_credit);

      if (!this.is_cashback) total = 0;

      return this.flt(total, this.currency_precision);
    },
    diff_payment() {
      let diff_payment = this.flt(
        this.invoice_doc.grand_total - this.total_payments,
        this.currency_precision
      );
      this.paid_change = -diff_payment;
      return diff_payment;
    },
    credit_change() {
      let change = -this.diff_payment;
      if (this.paid_change > change) return 0;
      return this.flt(this.paid_change - change, this.currency_precision);
    },
    diff_lable() {
      let lable = this.diff_payment < 0 ? 'Change' : 'To Be Paid';
      return lable;
    },
    available_pioints_amount() {
      let amount = 0;
      if (this.customer_info.loyalty_points) {
        amount =
          this.customer_info.loyalty_points *
          this.customer_info.conversion_factor;
      }
      return amount;
    },
    available_customer_credit() {
      let total = 0;
      this.customer_credit_dict.map((row) => {
        total += row.total_credit;
      });

      return total;
    },
    redeemed_customer_credit() {
      let total = 0;
      this.customer_credit_dict.map((row) => {
        if (flt(row.credit_to_redeem)) total += flt(row.credit_to_redeem);
        else row.credit_to_redeem = 0;
      });

      return total;
    },
    vaildatPayment() {
      if (this.pos_profile.posa_allow_sales_order) {
        if (
          this.invoiceType == 'Order' &&
          !this.invoice_doc.posa_delivery_date
        ) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
    request_payment_field() {
      let res = false;
      if (!this.pos_settings || this.pos_settings.invoice_fields.length == 0) {
        res = false;
      } else {
        this.pos_settings.invoice_fields.forEach((el) => {
          if (
            el.fieldtype == 'Button' &&
            el.fieldname == 'request_for_payment'
          ) {
            res = true;
          }
        });
      }
      return res;
    },
  },

  mounted: function () {
    this.$nextTick(function () {
      evntBus.$on('send_invoice_doc_payment', (invoice_doc) => {
        this.invoice_doc = invoice_doc;
        const default_payment = this.invoice_doc.payments.find(
          (payment) => payment.default == 1
        );
        this.is_credit_sale = 0;
        this.is_write_off_change = 0;
        if (default_payment) {
          default_payment.amount = this.flt(
            invoice_doc.grand_total,
            this.currency_precision
          );
        }
        this.loyalty_amount = 0;
        this.get_addresses();
        this.get_sales_person_names();
      });
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
        this.get_mpesa_modes();
      });
      evntBus.$on('add_the_new_address', (data) => {
        this.addresses.push(data);
        this.$forceUpdate();
      });
      evntBus.$on('update_invoice_type', (data) => {
        this.invoiceType = data;
        if (this.invoice_doc && data != 'Order') {
          this.invoice_doc.posa_delivery_date = null;
          this.invoice_doc.posa_notes = null;
          this.invoice_doc.shipping_address_name = null;
        }
      });
    });
    evntBus.$on('update_customer', (customer) => {
      if (this.customer != customer) {
        this.customer_credit_dict = [];
        this.redeem_customer_credit = false;
        this.is_cashback = true;
      }
    });
    evntBus.$on('set_pos_settings', (data) => {
      this.pos_settings = data;
    });
    evntBus.$on('set_customer_info_to_edit', (data) => {
      this.customer_info = data;
    });
    evntBus.$on('set_mpesa_payment', (data) => {
      this.set_mpesa_payment(data);
    });
    document.addEventListener('keydown', this.shortPay.bind(this));
  },
  beforeDestroy() {
    evntBus.$off('send_invoice_doc_payment');
    evntBus.$off('register_pos_profile');
    evntBus.$off('add_the_new_address');
    evntBus.$off('update_invoice_type');
    evntBus.$off('update_customer');
    evntBus.$off('set_pos_settings');
    evntBus.$off('set_customer_info_to_edit');
    evntBus.$off('update_invoice_coupons');
    evntBus.$off('set_mpesa_payment');
  },

  destroyed() {
    document.removeEventListener('keydown', this.shortPay);
  },

  watch: {
    loyalty_amount(value) {
      if (value > this.available_pioints_amount) {
        this.invoice_doc.loyalty_amount = 0;
        this.invoice_doc.redeem_loyalty_points = 0;
        this.invoice_doc.loyalty_points = 0;
        evntBus.$emit('show_mesage', {
          text: `Loyalty Amount can not be more then ${this.available_pioints_amount}`,
          color: 'error',
        });
      } else {
        this.invoice_doc.loyalty_amount = this.flt(this.loyalty_amount);
        this.invoice_doc.redeem_loyalty_points = 1;
        this.invoice_doc.loyalty_points =
          this.flt(this.loyalty_amount) / this.customer_info.conversion_factor;
      }
    },
    is_credit_sale(value) {
      if (value == 1) {
        this.invoice_doc.payments.forEach((payment) => {
          payment.amount = 0;
          payment.base_amount = 0;
        });
      }
    },
    is_write_off_change(value) {
      if (value == 1) {
        this.invoice_doc.write_off_amount = this.diff_payment;
        this.invoice_doc.write_off_outstanding_amount_automatically = 1;
      } else {
        this.invoice_doc.write_off_amount = 0;
        this.invoice_doc.write_off_outstanding_amount_automatically = 0;
      }
    },
    redeemed_customer_credit(value) {
      if (value > this.available_customer_credit) {
        evntBus.$emit('show_mesage', {
          text: `You can redeem customer credit upto ${this.available_customer_credit}`,
          color: 'error',
        });
      }
    },
    sales_person() {
      if (this.sales_person) {
        this.invoice_doc.sales_team = [
          {
            sales_person: this.sales_person,
            allocated_percentage: 100,
          },
        ];
      } else {
        this.invoice_doc.sales_team = [];
      }
    },
  },
};
</script>
