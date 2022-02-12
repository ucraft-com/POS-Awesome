<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5"
      style="max-height: 75vh; height: 75vh"
    >
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        top
        color="deep-purple accent-4"
      ></v-progress-linear>
      <v-row class="items px-2 py-1">
        <v-col cols="12" class="pb-0 mb-2">
          <v-text-field
            dense
            clearable
            autofocus
            outlined
            color="indigo"
            :label="frappe._('Search Items')"
            hint="Search by item code, serial number, batch no or barcode"
            background-color="white"
            hide-details
            v-model="debounce_search"
            @keydown.esc="esc_event"
            @keydown.enter="enter_event"
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="pt-0 mt-0">
          <div fluid class="items" v-if="items_view == 'card'">
            <v-row dense class="overflow-y-auto" style="max-height: 67vh">
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
                    :src="
                      item.image ||
                      '/assets/posawesome/js/posapp/components/pos/placeholder-image.png'
                    "
                    class="white--text align-end"
                    gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
                    height="100px"
                  >
                    <v-card-text
                      v-text="item.item_name"
                      class="text-subtitle-2 px-1 pb-2"
                    ></v-card-text>
                  </v-img>
                  <v-card-text class="text--primary pa-1">
                    <div class="text-caption indigo--text accent-3">
                      {{ item.rate || 0 }} {{ item.currency || '' }}
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </div>
          <div fluid class="items" v-if="items_view == 'list'">
            <div class="my-0 py-0 overflow-y-auto" style="max-height: 65vh">
              <template>
                <v-data-table
                  :headers="items_headers"
                  :items="filtred_items"
                  item-key="item_code"
                  class="elevation-1"
                  :items-per-page="itemsPerPage"
                  hide-default-footer
                  @click:row="add_item"
                >
                  <template v-slot:item.rate="{ item }">
                    {{ formtCurrency(item.rate) }}
                  </template>
                  <template v-slot:item.actual_qty="{ item }">
                    {{ formtCurrency(item.actual_qty) }}
                  </template>
                </v-data-table>
              </template>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="cards mb-0 mt-3 pa-2 grey lighten-5">
      <v-row no-gutters align="center" justify="center">
        <v-col cols="12">
          <v-select
            :items="items_group"
            :label="frappe._('Items Group')"
            dense
            outlined
            hide-details
            v-model="item_group"
          ></v-select>
        </v-col>
        <v-col cols="3" class="mt-1">
          <v-btn-toggle v-model="items_view" color="orange" group dense rounded>
            <v-btn small value="list">{{ __('List') }}</v-btn>
            <v-btn small value="card">{{ __('Card') }}</v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="4" class="mt-2">
          <v-btn small block color="warning" text @click="show_coupons"
            >{{ couponsCount }} {{ __('Coupons') }}</v-btn
          >
        </v-col>
        <v-col cols="5" class="mt-2">
          <v-btn small block color="warning" text @click="show_offers"
            >{{ offersCount }} {{ __('Offers') }} : {{ appliedOffersCount }}
            {{ __('Applied') }}</v-btn
          >
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>


<script>
import { evntBus } from '../../bus';
import _ from 'lodash';
export default {
  data: () => ({
    pos_profile: '',
    flags: {},
    items_view: 'list',
    item_group: 'ALL',
    loading: false,
    items_group: ['ALL'],
    items: [],
    search: '',
    first_search: '',
    itemsPerPage: 1000,
    items_headers: [
      { text: __('Name'), align: 'start', sortable: true, value: 'item_name' },
      { text: __('Rate'), value: 'rate', align: 'start' },
      { text: __('Available QTY'), value: 'actual_qty', align: 'start' },
      { text: __('UOM'), value: 'stock_uom', align: 'start' },
    ],
    offersCount: 0,
    appliedOffersCount: 0,
    couponsCount: 0,
    appliedCouponsCount: 0,
    customer_price_list: null,
  }),

  watch: {
    filtred_items(data_value) {
      this.update_items_details(data_value);
    },
    customer_price_list() {
      this.get_items();
    },
  },

  methods: {
    show_offers() {
      evntBus.$emit('show_offers', 'true');
    },
    show_coupons() {
      evntBus.$emit('show_coupons', 'true');
    },
    get_items() {
      if (!this.pos_profile) {
        console.log('No POS Profile');
        return;
      }
      const vm = this;
      this.loading = true;
      if (vm.pos_profile.posa_local_storage && localStorage.items_storage) {
        vm.items = JSON.parse(localStorage.getItem('items_storage'));
        evntBus.$emit('set_all_items', vm.items);
        vm.loading = false;
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_items',
        args: {
          pos_profile: vm.pos_profile,
          price_list: vm.customer_price_list,
        },
        callback: function (r) {
          if (r.message) {
            vm.items = r.message;
            evntBus.$emit('set_all_items', vm.items);
            vm.loading = false;
            console.info('loadItmes');
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('items_storage', '');
              localStorage.setItem('items_storage', JSON.stringify(r.message));
            }
          }
        },
      });
    },
    get_items_groups() {
      if (!this.pos_profile) {
        console.log('No POS Profile');
        return;
      }
      if (this.pos_profile.item_groups.length > 0) {
        this.pos_profile.item_groups.forEach((element) => {
          if (element.item_group !== 'All Item Groups') {
            this.items_group.push(element.item_group);
          }
        });
      } else {
        const vm = this;
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_items_groups',
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
      if (item.has_variants) {
        evntBus.$emit('open_variants_model', item, this.items);
      } else {
        evntBus.$emit('add_item', item);
      }
    },
    enter_event() {
      if (!this.filtred_items.length || !this.first_search) {
        return;
      }
      const qty = this.get_item_qty(this.first_search);
      const new_item = { ...this.filtred_items[0] };
      new_item.qty = flt(qty);
      new_item.item_barcode.forEach((element) => {
        if (this.search == element.barcode) {
          new_item.uom = element.posa_uom;
        }
      });
      if (this.flags.serial_no) {
        new_item.to_set_serial_no = this.flags.serial_no;
      }
      this.add_item(new_item);
      this.search = null;
      this.first_search = null;
      this.debounce_search = null;
      this.flags.serial_no = null;
    },
    get_item_qty(first_search) {
      let scal_qty = 1;
      if (first_search.startsWith(this.pos_profile.posa_scale_barcode_start)) {
        let pesokg1 = first_search.substr(7, 5);
        let pesokg;
        if (pesokg1.startsWith('0000')) {
          pesokg = '0.00' + pesokg1.substr(4);
        } else if (pesokg1.startsWith('000')) {
          pesokg = '0.0' + pesokg1.substr(3);
        } else if (pesokg1.startsWith('00')) {
          pesokg = '0.' + pesokg1.substr(2);
        } else if (pesokg1.startsWith('0')) {
          pesokg =
            pesokg1.substr(1, 1) + '.' + pesokg1.substr(2, pesokg1.length);
        } else if (!pesokg1.startsWith('0')) {
          pesokg =
            pesokg1.substr(0, 2) + '.' + pesokg1.substr(2, pesokg1.length);
        }
        scal_qty = pesokg;
      }
      return scal_qty;
    },
    get_search(first_search) {
      let search_term = '';
      if (
        first_search &&
        first_search.startsWith(this.pos_profile.posa_scale_barcode_start)
      ) {
        search_term = first_search.substr(0, 7);
      } else {
        search_term = first_search;
      }
      return search_term;
    },
    esc_event() {
      this.search = null;
      this.first_search = null;
    },
    update_items_details(items) {
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
                (element) => element.item_code == item.item_code
              );
              item.actual_qty = updated_item.actual_qty;
              item.serial_no_data = updated_item.serial_no_data;
              item.batch_no_data = updated_item.batch_no_data;
              item.item_uoms = updated_item.item_uoms;
            });
          }
        },
      });
    },
    update_cur_items_details() {
      this.update_items_details(this.filtred_items);
    },
    scan_barcoud() {
      const vm = this;
      onScan.attachTo(document, {
        suffixKeyCodes: [],
        keyCodeMapper: function (oEvent) {
          oEvent.stopImmediatePropagation();
          return onScan.decodeKeyEvent(oEvent);
        },
        onScan: function (sCode) {
          setTimeout(() => {
            vm.trigger_onscan(sCode);
          }, 300);
        },
      });
    },
    trigger_onscan(sCode) {
      if (this.filtred_items.length == 0) {
        evntBus.$emit('show_mesage', {
          text: `No Item has this barcode "${sCode}"`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
      } else {
        this.enter_event();
        this.debounce_search = null;
        this.search = null;
      }
    },
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
  },

  computed: {
    filtred_items() {
      this.search = this.get_search(this.first_search);
      let filtred_list = [];
      let filtred_group_list = [];
      if (this.item_group != 'ALL') {
        filtred_group_list = this.items.filter((item) =>
          item.item_group.toLowerCase().includes(this.item_group.toLowerCase())
        );
      } else {
        filtred_group_list = this.items;
      }
      if (!this.search || this.search.length < 3) {
        if (
          this.pos_profile.posa_show_template_items &&
          this.pos_profile.posa_hide_variants_items
        ) {
          return (filtred_list = filtred_group_list
            .filter((item) => !item.variant_of)
            .slice(0, 50));
        } else {
          return (filtred_list = filtred_group_list.slice(0, 50));
        }
      } else if (this.search) {
        filtred_list = filtred_group_list.filter((item) => {
          let found = false;
          for (let element of item.item_barcode) {
            if (element.barcode == this.search) {
              found = true;
              break;
            }
          }
          return found;
        });
        if (filtred_list.length == 0) {
          filtred_list = filtred_group_list.filter((item) =>
            item.item_code.toLowerCase().includes(this.search.toLowerCase())
          );
          if (filtred_list.length == 0) {
            filtred_list = filtred_group_list.filter((item) =>
              item.item_name.toLowerCase().includes(this.search.toLowerCase())
            );
          }
          if (
            filtred_list.length == 0 &&
            this.pos_profile.posa_search_serial_no
          ) {
            filtred_list = filtred_group_list.filter((item) => {
              let found = false;
              for (let element of item.serial_no_data) {
                if (element.serial_no == this.search) {
                  found = true;
                  this.flags.serial_no = null;
                  this.flags.serial_no = this.search;
                  break;
                }
              }
              return found;
            });
          }
        }
      }
      if (
        this.pos_profile.posa_show_template_items &&
        this.pos_profile.posa_hide_variants_items
      ) {
        return filtred_list.filter((item) => !item.variant_of).slice(0, 50);
      } else {
        return filtred_list.slice(0, 50);
      }
    },
    debounce_search: {
      get() {
        return this.first_search;
      },
      set: _.debounce(function (newValue) {
        this.first_search = newValue;
      }, 200),
    },
  },

  created: function () {
    this.$nextTick(function () {});
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
      this.get_items();
      this.get_items_groups();
    });
    evntBus.$on('update_cur_items_details', () => {
      this.update_cur_items_details();
    });
    evntBus.$on('update_offers_counters', (data) => {
      this.offersCount = data.offersCount;
      this.appliedOffersCount = data.appliedOffersCount;
    });
    evntBus.$on('update_coupons_counters', (data) => {
      this.couponsCount = data.couponsCount;
      this.appliedCouponsCount = data.appliedCouponsCount;
    });
    evntBus.$on('update_customer_price_list', (data) => {
      this.customer_price_list = data;
    });
  },

  mounted() {
    this.scan_barcoud();
  },
};
</script>

<style scoped>
</style>