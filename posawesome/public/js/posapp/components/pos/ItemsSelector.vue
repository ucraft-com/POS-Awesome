<template>
  <div>
    <v-card class="selection mx-auto grey lighten-5" style="max-height: 80vh; height: 80vh">
      <v-row class="items px-2 py-1">
        <v-col cols="12" class="pb-0 mb-2">
          <v-text-field
            dense
            clearable
            autofocus
            outlined
            color="indigo"
            label="Serch Items"
            hint="Search by item code, serial number, batch no or barcode"
            background-color="white"
            hide-details
            v-model="search"
            @keydown.enter="enter_event"
            @keydown.esc="esc_event"
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="pt-0 mt-0">
          <div fluid class="items" v-if="items_view=='card'">
            <v-row dense class="overflow-y-auto" style="max-height: 68vh">
              <v-progress-linear
                :active="loading"
                :indeterminate="loading"
                absolute
                top
                color="deep-purple accent-4"
              ></v-progress-linear>
              <v-col
                v-for="(item, idx) in filtred_items"
                :key="idx"
                xl="2"
                lg="3"
                md="6"
                sm="6"
                cols="6"
                min-height="50"
              >
                <v-card hover="hover" @click="add_item(item)">
                  <v-img
                    :src="item.image || 'https://lunawood.com/wp-content/uploads/2018/02/placeholder-image.png'"
                    class="white--text align-end"
                    gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
                    height="100px"
                  >
                    <v-card-text v-text="item.item_name" class="text-subtitle-2 px-1 pb-2"></v-card-text>
                  </v-img>
                  <v-card-text class="text--primary pa-1">
                    <div
                      class="text-caption indigo--text accent-3"
                    >{{ item.price_list_rate || 0}} {{ item.currency || ''}}</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </div>
          <div fluid class="items" v-if="items_view=='list'">
            <div class="my-0 py-0 overflow-y-auto" style="max-height: 68vh">
              <template>
                <v-data-table
                  :headers="items_headers"
                  :items="filtred_items"
                  item-key="item_code"
                  class="elevation-1"
                  :items-per-page="itemsPerPage"
                  hide-default-footer
                  @click:row="add_item"
                ></v-data-table>
              </template>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card>
    <v-card style="max-height: 10vh; height: 10vh" class="cards mb-0 mt-3 pa-2 grey lighten-5">
      <v-row no-gutters>
        <v-col cols="12">
          <v-select
            :items="items_group"
            label="Items Group"
            dense
            outlined
            hide-details
            v-model="item_group"
          ></v-select>
        </v-col>
        <v-col cols="8" class="mt-1">
          <v-btn-toggle v-model="items_view" color="primary accent-3" group dense rounded>
            <v-btn value="card">Card View</v-btn>
            <v-btn value="list">List View</v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="4" class="mt-1">
          <v-btn-toggle v-model="favourites_view" color="success accent-3" group dense rounded>
            <v-btn value="True">Favourites</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>


<script>
import { evntBus } from "../../bus";
export default {
  // props: ["pos_profile"],
  data: () => ({
    pos_profile: "",
    items_view: "list",
    item_group: "ALL",
    favourites_view: false,
    loading: false,
    items_group: ["ALL"],
    items: [],
    search: "",
    itemsPerPage: 1000,
    items_headers: [
      { text: "Name", align: "start", sortable: true, value: "item_name" },
      { text: "UOM", value: "stock_uom", align: "start" },
      { text: "Currency", value: "currency", align: "start" },
      { text: "Rate", value: "price_list_rate", align: "start" },
    ],
  }),
  // watch: {
  //   pos_profile() {
  //     console.log("POS Profile Updated")
  //     this.get_items();
  //     this.get_items_groups();
  //   },
  // },

  methods: {
    get_items() {
      if (!this.pos_profile) {
        console.log("No POS Profile");
        return;
      }
      const vm = this;
      this.loading = true;
      if (localStorage.items_storage) {
        vm.items = JSON.parse(localStorage.getItem("items_storage"));
        vm.loading = false;
      }
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_items",
        args: { pos_profile: vm.pos_profile },
        callback: function (r) {
          if (r.message) {
            const loadItmes =
              !localStorage.items_storage ||
              JSON.parse(localStorage.getItem("items_storage")).length !=
                r.message.length;
            localStorage.setItem("items_storage", "");
            localStorage.setItem("items_storage", JSON.stringify(r.message));
            if (loadItmes) {
              vm.$nextTick(() => {
                console.log("loadItmes", loadItmes);
                vm.items = JSON.parse(localStorage.getItem("items_storage"));
                vm.loading = false;
              });
            }
          }
        },
      });
    },
    get_items_groups() {
      if (!this.pos_profile) {
        console.log("No POS Profile");
        return;
      }
      if (this.pos_profile.item_groups.length > 0) {
        this.pos_profile.item_groups.forEach((element) => {
          if (element.item_group !== "All Item Groups") {
            this.items_group.push(element.item_group);
          }
        });
      } else {
        const vm = this;
        frappe.call({
          method: "posawesome.posawesome.api.posapp.get_items_groups",
          args: {},
          callback: function (r) {
            if (r.message) {
              r.message.forEach((element) => {
                vm.items_group.push(element.name);
              });
            }
          },
        });
      }
    },
    add_item(item) {
      evntBus.$emit("add_item", item);
    },
    enter_event() {
      if (!this.filtred_items.length || !this.search) {
        return;
      }
      this.add_item(this.filtred_items[0]);
      this.search = null;
    },
    esc_event() {
      this.search = null;
    },
  },
  computed: {
    filtred_items() {
      let filtred_list = [];
      let filtred_group_list = [];
      if (this.item_group != "ALL") {
        filtred_group_list = this.items.filter((item) =>
          item.item_group.toLowerCase().includes(this.item_group.toLowerCase())
        );
      } else {
        filtred_group_list = this.items;
      }
      if (!this.search || this.search.length < 3) {
        return (filtred_list = filtred_group_list.slice(0, 100));
      } else if (this.search) {
        filtred_list = filtred_group_list.filter((item) => {
          let found = false;
          for (let element of item.item_barcode) {
            if (element.barcode == this.search) {
              found = true;
              break;
            }
            console.log(element.barcode);
          }
        });
        if (filtred_list.length == 0) {
          filtred_list = filtred_group_list.filter((item) =>
            item.item_name.toLowerCase().includes(this.search.toLowerCase())
          );
          if (filtred_list.length == 0) {
            filtred_list = filtred_group_list.filter((item) =>
              item.item_code.toLowerCase().includes(this.search.toLowerCase())
            );
          }
        }
      }
      return filtred_list.slice(0, 100);
    },
  },

  created: function () {
    this.$nextTick(function () {});
    evntBus.$on("register_pos_profile", (pos_profile) => {
      this.pos_profile = pos_profile;
      this.get_items();
      this.get_items_groups();
    });
  },
  // mounted() {
  //   if (localStorage.getItem('items_storage')) {
  //     try {
  //       this.items = JSON.parse(localStorage.getItem('items_storage'));
  //     } catch(e) {
  //       // localStorage.removeItem('cats');
  //       console.log(e)
  //     }
  //   }
  // },
};
</script>

<style scoped>
</style>