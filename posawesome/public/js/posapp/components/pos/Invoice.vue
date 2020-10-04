<template>
  <div>
    <v-card
      style="max-height: 70vh; height: 70vh"
      class="cards my-0 py-0 grey lighten-5"
    >
      <Customer></Customer>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 59vh">
        <template @mouseover="style = 'cursor: pointer'">
          <v-data-table
            :headers="items_headers"
            :items="items"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            item-key="item_code"
            show-expand
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.amount="{ item }">{{
              item.qty * item.rate
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
                      readonly
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
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      label="UOM"
                      background-color="white"
                      hide-details
                      v-model="item.stock_uom"
                      readonly
                    ></v-text-field>
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
                      :disabled="item.pricing_rules ? true : false"
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
                      readonly
                      :prefix="invoice_doc.currency"
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
                      :disabled="item.pricing_rules ? true : false"
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
                      :disabled="item.pricing_rules ? true : false"
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
                      readonly
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
                      readonly
                    ></v-text-field>
                  </v-col>
                  <!-- <v-col cols="12">
                    <p>More info about {{ item.name }} {{ item }}</p>
                  </v-col> -->
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
          style="max-height: 20vh; height: 20vh"
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
                    v-model="additional_discount"
                    label="ِAdditional Discount"
                    outlined
                    dense
                    hide-details
                    type="number"
                    :prefix="pos_profile.currency"
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
                    disabled
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
                    disabled
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
          style="max-height: 20vh; height: 20vh"
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
      invoice_doc: "",
      customer: "",
      customer_info: "",
      additional_discount: 0,
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
        { text: "UOM", value: "stock_uom", align: "center" },
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
      return flt(qty);
    },
    subtotal() {
      this.close_payments();
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      return flt(sum);
    },
    total_items_discount_amount() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.discount_amount;
      });
      return flt(sum);
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
      // this.$forceUpdate();
    },
    subtract_one(item) {
      item.qty--;
      if (item.qty <= 0) {
        this.remove_item(item);
      }
      // this.$forceUpdate();
    },
    add_item(item) {
      const index = this.items.findIndex(
        (el) => el.item_code === item.item_code
      );
      if (index === -1) {
        const new_item = { ...item };
        new_item.qty = 1;
        new_item.discount_amount = 0;
        new_item.discount_percentage = 0;
        item.discount_amount_per_item = 0;
        new_item.price_list_rate = item.rate;
        this.items.unshift(new_item);
        this.update_item_detail(new_item);
      } else {
        this.update_items_details([this.items[index]]);
        this.items[index].qty++;
        this.items[index].actual_qty = item.actual_qty;
      }
    },
    cancel_invoice() {
      const doc = this.get_invoice_doc();
      if (doc.name) {
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
    },
    new_invoice(data = {}) {
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
      } else {
        this.invoice_doc = data;
        this.items = data.items;
        this.customer = data.customer;
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
      (doc.posa_pos_opening_shift = this.pos_opening_shift.name),
        (doc.payments = doc.payments = this.get_payments()),
        (doc.taxes = []);
      return doc;
    },
    get_invoice_items() {
      const items_list = [];
      this.items.forEach((item) => {
        items_list.push({
          item_code: item.item_code,
          qty: item.qty,
          rate: item.rate,
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
      evntBus.$emit("show_payment", "true");
      const invoice_doc = this.proces_invoice();
      invoice_doc.customer_info = this.customer_info;
      evntBus.$emit("send_invoice_doc_payment", invoice_doc);
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
                (element) => element.item_code == item.item_code
              );
              item.actual_qty = updated_item.actual_qty;
              item.serial_no_data = updated_item.serial_no_data;
              item.batch_no_data = updated_item.batch_no_data;
              item.uoms = updated_item.uoms;
              item.rate = updated_item.rate;
              item.currency = updated_item.currency;
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
            plc_conversion_rate: 1,
            pos_profile: this.pos_profile.name,
            price_list: this.pos_profile.selling_price_list,
            stock_uom: item.uom,
            tax_category: "",
            transaction_type: "selling",
            update_stock: 1,
          },
        },
        callback: function (r) {
          if (r.message) {
            const data = r.message;
            item.discount_amount_on_rate = data.discount_amount_on_rate;
            item.discount_amount_on_rate = data.discount_amount_on_rate;
            item.discount_percentage = data.discount_percentage;
            item.discount_percentage_on_rate = data.discount_percentage_on_rate;
            item.discount_amount = data.discount_amount || 0;
            item.has_pricing_rule = data.has_pricing_rule;
            item.last_purchase_rate = data.last_purchase_rate;
            item.price_list_rate = data.price_list_rate;
            item.price_or_product_discount = data.price_or_product_discount;
            item.pricing_rule_for = data.pricing_rule_for;
            item.pricing_rules = data.pricing_rules;
            item.projected_qty = data.projected_qty;
            item.reserved_qty = data.reserved_qty;
            item.batch_no = data.batch_no;
            item.actual_qty = data.actual_qty;
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
          item.discount_amount = flt(item.price_list_rate) - flt(value);
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
          item.rate =
            flt(item.price_list_rate) -
            (flt(item.price_list_rate) * flt(value)) / 100;
          item.discount_amount = flt(item.price_list_rate) - flt(item.rate);
        }
      }
    },
    calc_item_price(item) {
      if (!item.has_pricing_rule) {
        return;
      }
      if (item.discount_percentage) {
        item.rate =
          flt(item.price_list_rate) -
          (flt(item.price_list_rate) * flt(item.discount_percentage)) / 100;
        item.discount_amount = flt(item.price_list_rate) - flt(item.rate);
        item.discount_amount = flt(item.price_list_rate) - flt(item.rate);
      } else if (item.discount_amount) {
        item.rate = flt(item.price_list_rate) - flt(item.discount_amount);
      } else if (item.pricing_rule_for === "Rate") {
        item.rate = item.price_list_rate;
      }
    },
  },
  created() {
    this.$nextTick(function () {});
    evntBus.$on("register_pos_profile", (data) => {
      this.pos_profile = data.pos_profile;
      this.customer = data.pos_profile.customer;
      this.pos_opening_shift = data.pos_opening_shift;
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
      // this.get_loyalty();
    },
    expanded(data_value) {
      this.update_items_details(data_value);
    },
  },
};
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
</style>