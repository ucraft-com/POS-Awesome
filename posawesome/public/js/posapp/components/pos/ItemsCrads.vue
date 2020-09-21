<template>
  <div>
    <v-card style="max-height: 70vh; height: 70vh" class="cards my-0 py-0 grey lighten-5">
      <Customer></Customer>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 59vh">
        <template>
          <v-data-table
            :headers="items_headers"
            :items="items"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            item-key="name"
            show-expand
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.subtract="{ item }">
              <v-btn icon small color="indigo lighten-1" @click.stop="subtract_one(item)">
                <v-icon>mdi-minus-circle-outline</v-icon>
              </v-btn>
            </template>
            <template v-slot:item.add="{ item }">
              <v-btn icon small color="indigo lighten-1" @click.stop="add_one(item)">
                <v-icon>mdi-plus-circle-outline</v-icon>
              </v-btn>
            </template>
            <template v-slot:item.total="{ item }">{{ item.qty * item.price }}</template>
            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length">More info about {{ item.name }}</td>
            </template>
          </v-data-table>
        </template>
      </div>
    </v-card>
    <v-row>
      <v-col class="pt-0 pr-0" cols="8">
        <v-card style="max-height: 20vh; height: 20vh" class="cards mb-0 mt-3 py-0 grey lighten-5">
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
                  <v-text-field v-model="total" label="Total" outlined dense readonly hide-details></v-text-field>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col class="pt-0 pr-3" cols="4">
        <v-card flat style="max-height: 20vh; height: 20vh" class="cards mb-0 mt-3 py-0">
          <v-row align="start" style="height: 53%">
            <v-col cols="12">
              <v-btn block class="pa-0" large color="warning" dark>Get Hold Invoice</v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn block class="pa-0" large color="error" dark @click="cancel_invoice">Cancel</v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn block class="pa-0" large color="success" dark>New</v-btn>
            </v-col>
          </v-row>
          <v-row align="end" style="height: 54%">
            <v-col cols="12">
              <v-btn block class="pa-0" large color="primary" dark>PAY</v-btn>
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
  props: [
    // "items"
  ],
  data() {
    return {
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
        { text: "", value: "subtract", align: "center" },
        { text: "QTY", value: "qty", align: "center" },
        { text: "", value: "add", align: "center" },
        { text: "Price", value: "price", align: "center" },
        { text: "VAT", value: "vat", align: "center" },
        { text: "Total", value: "total", align: "center" },
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
        sum += item.qty * item.price;
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
      const index = this.items.findIndex((el) => el.name === item.name);
      if (index === -1) {
        const new_item = { ...item };
        new_item.qty = 1;
        new_item.vat = 18;
        new_item.price = 25;
        (new_item.active = false), this.items.unshift(new_item);
      } else {
        this.items[index].qty++;
      }
    },
    cancel_invoice() {
      this.items = []
    },
  },
  created() {
    evntBus.$on("add_item", (item) => {
      this.add_item(item);
    });
  },
  mounted: function () {
    // this.$nextTick(function () {
    // const vm = this;
    //     frappe.call({
    //         method: 'roxtools.roxtools.doctype.myprojects.myprojects.get_all_projects',
    //         async: false,
    //         callback: function(r) {
    //             if (r.message) {
    //                 // console.log(r.message);
    //                 vm.projects = r.message;
    //             }
    //         }
    //     });
    // })
    // this.$nextTick(function () {
    //     const vm = this;
    //     frappe.realtime.on('rox_add_project', function(data) {
    //         vm.projects.push(data);
    //     });
    // })
  },
};
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
</style>