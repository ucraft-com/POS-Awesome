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
                    <p>More info about {{ item.name }} {{ expanded }}</p>
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
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="subtotal"
                    label="Subtotal"
                    outlined
                    dense
                    readonly
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="items_discount"
                    label="Items Discount"
                    outlined
                    dense
                    readonly
                    hide-details
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
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="total_tax"
                    label="TAX"
                    outlined
                    dense
                    readonly
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="total"
                    label="Total"
                    outlined
                    dense
                    readonly
                    hide-details
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
              <v-btn block class="pa-0" large color="warning" dark
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
              <v-btn block class="pa-0" large color="success" dark>New</v-btn>
            </v-col>
          </v-row>
          <v-row align="end" style="height: 54%">
            <v-col cols="12">
              <v-btn
                block
                class="pa-0"
                large
                color="primary"
                @click="save_invoice"
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
      doc: "",
      customer: "",
      items_discount: 0,
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
          sortable: false,
          value: "item_name",
        },
        { text: "QTY", value: "qty", align: "center" },
        { text: "UOM", value: "stock_uom", align: "center" },
        { text: "Rate", value: "rate", align: "center" },
        // { text: "VAT", value: "vat", align: "center" },
        { text: "Amount", value: "amount", align: "center" },
      ],
    };
  },
  components: {
    Customer,
  },
  computed: {
    total_qty() {
      let qty = 0;
      this.items.forEach((item) => {
        qty += item.qty;
      });
      return qty;
    },
    subtotal() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      return sum;
    },
  },
  methods: {
    // sortBy(prop) {
    //   this.projects.sort((a, b) => (a[prop] < b[prop] ? -1 : 1));
    // },
    remove_item(item) {
      const index = this.items.findIndex((el) => el === item);
      this.items.splice(index, 1);
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
        // new_item.vat = 18;
        (new_item.active = false), this.items.unshift(new_item);
      } else {
        this.items[index].qty++;
      }
    },
    cancel_invoice() {
      this.items = [];
      this.customer = this.pos_profile.customer;
    },
    save_invoice() {
      const vm = this;
      const doc = this.get_invoice_doc();
      frappe.call({
        method: "posawesome.posawesome.api.posapp.save_invoice",
        args: { data: doc },
        async: false,
        callback: function (r) {
          if (r.message) {
            console.log(r.message);
            vm.submit_invoice(r.message);
          }
        },
      });
    },
    get_invoice_doc() {
      const doc = {};
      doc.doctype = "Sales Invoice";
      doc.is_pos = 1;
      doc.company = this.pos_profile.company;
      doc.pos_profile = this.pos_profile.name;
      doc.currency = this.pos_profile.currency;
      doc.naming_series = this.pos_profile.naming_series;
      doc.customer = this.customer;
      doc.items = this.get_invoice_items();
      doc.total = this.subtotal;
      (doc.payments = []), (doc.taxes = []);
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
          amount = this.subtotal; // NOTE : this shoulde update from user
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
    submit_invoice(doc) {
      doc.payments = this.get_payments();
      frappe.call({
        method: "posawesome.posawesome.api.posapp.submit_invoice",
        args: { data: doc },
        async: false,
        callback: function (r) {
          if (r.message) {
            console.log(r.message);
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
    });
    evntBus.$on("add_item", (item) => {
      this.add_item(item);
    });
    evntBus.$on("update_customer", (customer) => {
      this.customer = customer;
    });
  },
  mounted: function () {},
  watch: {
    customer() {
      evntBus.$emit("set_customer", this.customer);
    },
  },
};
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
</style>