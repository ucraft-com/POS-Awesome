<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5"
      style="max-height: 78vh; height: 78vh"
    >
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        top
        color="deep-purple accent-4"
      ></v-progress-linear>
      <div class="overflow-y-auto px-2 pt-2" style="max-height: 78vh">
        <v-row v-if="invoice_doc" class="px-1 py-0">
          <v-col cols="7">
            <v-text-field
              outlined
              color="indigo"
              label="Paid Amount"
              background-color="white"
              hide-details
              :value="formtCurrency(total_payments)"
              readonly
              :prefix="invoice_doc.currency"
              dense
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              outlined
              color="indigo"
              :label="diff_lable"
              background-color="white"
              hide-details
              :value="formtCurrency(diff_payment)"
              disabled
              :prefix="invoice_doc.currency"
              dense
            ></v-text-field>
          </v-col>

          <v-col cols="7" v-if="diff_payment < 0 && !invoice_doc.is_return">
            <v-text-field
              outlined
              color="indigo"
              label="Paid Change"
              background-color="white"
              v-model="paid_change"
              @input="set_paid_change()"
              :prefix="invoice_doc.currency"
              :rules="paid_change_rules"
              dense
              type="number"
            ></v-text-field>
          </v-col>

          <v-col cols="5" v-if="diff_payment < 0 && !invoice_doc.is_return">
            <v-text-field
              outlined
              color="indigo"
              label="Credit Change"
              background-color="white"
              hide-details
              :value="formtCurrency(credit_change)"
              disabled
              :prefix="invoice_doc.currency"
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
            <v-col cols="7">
              <v-text-field
                dense
                outlined
                color="indigo"
                :label="payment.mode_of_payment"
                background-color="white"
                hide-details
                v-model="payment.amount"
                type="number"
                :prefix="invoice_doc.currency"
                @focus="set_rest_amount(payment.idx)"
                :readonly="invoice_doc.is_return ? true : false"
              ></v-text-field>
            </v-col>
            <v-col cols="5">
              <v-btn
                block
                class=""
                color="primary"
                dark
                @click="set_full_amount(payment.idx)"
                >{{ payment.mode_of_payment }}</v-btn
              >
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
              color="indigo"
              label="Redeem Loyalty Points"
              background-color="white"
              hide-details
              v-model="loyalty_amount"
              type="number"
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="You can redeem upto"
              background-color="white"
              hide-details
              :value="formtCurrency(available_pioints_amount)"
              :prefix="invoice_doc.currency"
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
              color="indigo"
              label="Redeemed Customer Credit"
              background-color="white"
              hide-details
              v-model="redeemed_customer_credit"
              type="number"
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="You can redeem credit upto"
              background-color="white"
              hide-details
              :value="formtCurrency(available_customer_credit)"
              :prefix="invoice_doc.currency"
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
              color="indigo"
              label="Net Total"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.net_total)"
              disabled
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="Tax and Charges"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.total_taxes_and_charges)"
              disabled
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="Totoal Amount"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.total)"
              disabled
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="Discount Amount"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.discount_amount)"
              disabled
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              dense
              outlined
              color="indigo"
              label="Grand Amount"
              background-color="white"
              hide-details
              :value="formtCurrency(invoice_doc.grand_total)"
              disabled
              :prefix="invoice_doc.currency"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row class="px-1 py-0">
          <v-col cols="6 my-0 py-0">
            <v-switch
              v-if="
                pos_profile.posa_allow_credit_sale && !invoice_doc.is_return
              "
              v-model="is_credit_sale"
              flat
              label="Is Credit Sale"
              class="my-0 py-0"
            ></v-switch>

            <v-switch
              v-if="invoice_doc.is_return && pos_profile.use_cashback"
              v-model="is_cashback"
              flat
              label="Is Cashback"
              class="my-0 py-0"
            ></v-switch>
          </v-col>
          <v-col cols="6">
            <v-menu
              v-if="is_credit_sale"
              ref="date_menu"
              v-model="date_menu"
              :close-on-content-click="false"
              :return-value.sync="invoice_doc.due_date"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="invoice_doc.due_date"
                  label="Due Date"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="invoice_doc.due_date" no-title scrollable>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="date_menu = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="
                    [
                      $refs.date_menu.save(invoice_doc.due_date),
                      validate_due_date(),
                    ]
                  "
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-switch
              v-if="!invoice_doc.is_return && pos_profile.use_customer_credit"
              v-model="redeem_customer_credit"
              flat
              label="Use Customer Credit"
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
                color="indigo"
                label="Available Credit"
                background-color="white"
                hide-details
                :value="formtCurrency(row.total_credit)"
                disabled
                :prefix="invoice_doc.currency"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="indigo"
                label="Redeem Credit"
                background-color="white"
                hide-details
                type="number"
                v-model="row.credit_to_redeem"
                :prefix="invoice_doc.currency"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>
      </div>
    </v-card>

    <v-card
      flat
      style="max-height: 11vh; height: 11vh"
      class="cards mb-0 mt-3 py-0"
    >
      <v-row align="start" no-gutters>
        <v-col cols="12">
          <v-btn
            block
            class="pa-1"
            large
            color="warning"
            dark
            @click="back_to_invoice"
            >Back</v-btn
          >
        </v-col>
        <v-col cols="12">
          <v-btn block class="mt-2" large color="primary" dark @click="submit"
            >Submit Payments</v-btn
          >
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    loading: false,
    pos_profile: '',
    invoice_doc: '',
    loyalty_amount: 0,
    is_credit_sale: 0,
    date_menu: false,
    paid_change: 0,
    paid_change_rules: [],
    is_return: false,
    is_cashback: true,
    redeem_customer_credit: false,
    customer_credit_dict: [],
  }),

  methods: {
    back_to_invoice() {
      evntBus.$emit('show_payment', 'false');
      evntBus.$emit('set_customer_readonly', false);
    },
    submit() {
      if (!this.invoice_doc.is_return && this.total_payments < 0) {
        evntBus.$emit('show_mesage', {
          text: `Payments not correct`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
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

      let total_change =
        parseInt(this.paid_change) + parseInt(-this.credit_change);

      if (this.is_cashback && total_change != -this.diff_payment) {
        evntBus.$emit('show_mesage', {
          text: `Error in change calculations!`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
        return;
      }

      let credit_calc_check = this.customer_credit_dict.filter((row) => {
        if (row.credit_to_redeem)
          return row.credit_to_redeem > row.total_credit;
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

      this.submit_invoice();
      this.customer_credit_dict = [];
      this.redeem_customer_credit = false;
      this.is_cashback = true;

      evntBus.$emit('new_invoice', 'false');
      this.back_to_invoice();
    },
    submit_invoice() {
      let formData = this.invoice_doc;
      formData['total_change'] = -this.diff_payment;
      formData['paid_change'] = this.paid_change;
      formData['credit_change'] = -this.credit_change;
      formData['redeemed_customer_credit'] = this.redeemed_customer_credit;
      formData['customer_credit_dict'] = this.customer_credit_dict;
      formData['is_cashback'] = this.is_cashback;

      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.submit_invoice',
        args: {
          data: formData,
        },
        async: true,
        callback: function (r) {
          if (r.message) {
            vm.load_print_page();
            evntBus.$emit('show_mesage', {
              text: `Invoice ${r.message.name} is Submited`,
              color: 'success',
            });
            frappe.utils.play_sound('submit');
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
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
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
      if (e) {
        frappe
          .call(
            'posawesome.posawesome.api.posapp_customization.get_available_credit',
            {
              customer: this.invoice_doc.customer,
            }
          )
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
  },

  computed: {
    total_payments() {
      let total = flt(this.invoice_doc.loyalty_amount);
      this.invoice_doc.payments.forEach((payment) => {
        total += flt(payment.amount);
      });

      total += flt(this.redeemed_customer_credit);

      if (!this.is_cashback) total = 0;

      return total.toFixed(2);
    },
    diff_payment() {
      let diff_payment = (
        this.invoice_doc.grand_total - this.total_payments
      ).toFixed(2);
      this.paid_change = -diff_payment;
      return diff_payment;
    },
    credit_change() {
      let change = -this.diff_payment;
      if (this.paid_change > change) return 0;
      return (this.paid_change - change).toFixed(2);
    },
    diff_lable() {
      let lable = this.diff_payment < 0 ? 'Change' : 'To Be Paid';
      return lable;
    },
    available_pioints_amount() {
      let amount = 0;
      if (this.invoice_doc.customer_info.loyalty_points) {
        amount =
          this.invoice_doc.customer_info.loyalty_points *
          this.invoice_doc.customer_info.conversion_factor;
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
        if (row.credit_to_redeem) total += parseFloat(row.credit_to_redeem);
        else row.credit_to_redeem = 0;
      });

      return total;
    },
  },

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('send_invoice_doc_payment', (invoice_doc) => {
        this.invoice_doc = invoice_doc;
        const default_payment = this.invoice_doc.payments.find(
          (payment) => payment.default == 1
        );
        this.is_credit_sale = 0;
        if (default_payment) {
          default_payment.amount = invoice_doc.grand_total.toFixed(2);
        }
        this.loyalty_amount = 0;
      });
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
      });
    });
    evntBus.$on('update_customer', (customer) => {
      if (this.customer != customer) {
        this.customer_credit_dict = [];
        this.redeem_customer_credit = false;
        this.is_cashback = true;
      }
    });
    document.addEventListener('keydown', this.shortPay.bind(this));
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
        this.invoice_doc.loyalty_amount = flt(this.loyalty_amount);
        this.invoice_doc.redeem_loyalty_points = 1;
        this.invoice_doc.loyalty_points =
          flt(this.loyalty_amount) *
          this.invoice_doc.customer_info.conversion_factor;
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
    redeemed_customer_credit(value) {
      if (value > this.available_customer_credit) {
        evntBus.$emit('show_mesage', {
          text: `You can redeem customer credit upto ${this.available_customer_credit}`,
          color: 'error',
        });
      }
    },
  },
};
</script>
