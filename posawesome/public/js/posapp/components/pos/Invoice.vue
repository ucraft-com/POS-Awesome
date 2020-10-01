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
              <td :colspan="headers.length">
                <v-row>
                  <v-col cols="1">
                    <v-btn
                      icon
                      small
                      color="red"
                      @click.stop="remove_item(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="1">
                    <v-btn
                      icon
                      small
                      color="indigo lighten-1"
                      @click.stop="subtract_one(item)"
                    >
                      <v-icon>mdi-minus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="1">
                    <v-btn
                      icon
                      small
                      color="indigo lighten-1"
                      @click.stop="add_one(item)"
                    >
                      <v-icon>mdi-plus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6">
                    <p>More info about {{ item.name }} {{ item }}</p>
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
                <!-- <v-col cols="12">
                  <v-text-field
                    v-model="subtotal"
                    label="Subtotal"
                    outlined
                    dense
                    readonly
                    hide-details
                  ></v-text-field>
                </v-col> -->
                <v-col cols="12">
                  <v-text-field
                    v-model="items_discounts"
                    label="Items Discounts"
                    outlined
                    dense
                    readonly
                    hide-details
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
                    v-model="additional_discount"
                    label="ِAdditional Discount"
                    outlined
                    dense
                    hide-details
                    type="number"
                    :prefix="pos_profile.currency"
                  ></v-text-field>
                </v-col>
                <!-- <v-col cols="12">
                  <v-text-field
                    v-model="total_tax"
                    label="TAX"
                    outlined
                    dense
                    readonly
                    hide-details
                  ></v-text-field>
                </v-col> -->
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
      items_discounts: 0,
      additional_discount: 0,
      total_tax: 0,
      total: 0,
      items: [],
      itemsPerPage: 1000,
      expanded: [],
      singleExpand: false,
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
        this.update_items_details([new_item]);
        this.items.unshift(new_item);
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
              frappe.show_alert(
                // TODO : replace whith proper alert
                {
                  message: __(`${r.message}`),
                  indicator: "green",
                },
                5
              );
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
        let amount = 0;
        if (payment.mode_of_payment === "Cash") {
          amount = this.subtotal; // NOTE : this shoulde updated from user
        }
        payments.push({
          amount: amount,
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
        frappe.throw(__("There is no Customer!")); // TODO : replace whith proper alert
        return;
      }
      if (!this.items.length) {
        frappe.throw(__("There is no Items!")); // TODO : replace whith proper alert
        return;
      }
      evntBus.$emit("show_payment", "true");
      const invoice_doc = this.proces_invoice();
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