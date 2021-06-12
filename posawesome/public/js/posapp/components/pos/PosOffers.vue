<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5"
      style="max-height: 80vh; height: 80vh"
    >
      <v-card-title>
        <span class="text-h6 warning--text">POS Offers</span>
      </v-card-title>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 75vh">
        <template @mouseover="style = 'cursor: pointer'">
          <v-data-table
            :headers="items_headers"
            :items="pos_offers"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            show-expand
            item-key="row_id"
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.offer_applied="{ item }">
              <v-simple-checkbox
                @click="forceUpdateItem"
                v-model="item.offer_applied"
                :disabled="!item.give_item"
              ></v-simple-checkbox>
            </template>
            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length">
                <v-row class="mt-2">
                  <v-col v-if="item.description">
                    <div
                      class="indigo--text"
                      v-html="handleNewLine(item.description)"
                    ></div>
                  </v-col>
                  <v-col v-if="item.offer == 'Give Product'">
                    <v-autocomplete
                      v-model="item.give_item"
                      :items="get_give_items(item)"
                      item-text="item_code"
                      outlined
                      dense
                      color="indigo"
                      label="Give Item"
                      :disabled="item.apply_type != 'Item Group'"
                    ></v-autocomplete>
                  </v-col>
                </v-row>
              </td>
            </template>
          </v-data-table>
        </template>
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
    pos_offers: [],
    itemsPerPage: 1000,
    expanded: [],
    singleExpand: true,
    items_headers: [
      { text: 'Name', value: 'name', align: 'start' },
      { text: 'Apply On', value: 'apply_on', align: 'start' },
      { text: 'Offer', value: 'offer', align: 'start' },
      { text: 'Applied', value: 'offer_applied', align: 'start' },
    ],
  }),

  computed: {},

  methods: {
    back_to_invoice() {
      evntBus.$emit('show_offers', 'false');
    },
    forceUpdateItem() {
      const list_offers = [...this.pos_offers];
      this.pos_offers = list_offers;
    },
    makeid(length) {
      let result = '';
      const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
      const charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
    updatePosOffers(offers) {
      const toRemove = [];
      this.pos_offers.forEach((pos_offer) => {
        const offer = offers.find((offer) => offer.name === pos_offer.name);
        if (!offer) {
          toRemove.push(pos_offer.row_id);
        }
      });
      this.removeOffers(toRemove);
      offers.forEach((offer) => {
        const pos_offer = this.pos_offers.find(
          (pos_offer) => offer.name === pos_offer.name
        );
        if (pos_offer) {
          pos_offer.items = offer.items;
        } else {
          if (!offer.row_id) {
            offer.row_id = this.makeid(20);
          }
          if (offer.apply_type == 'Item Code') {
            offer.give_item = offer.apply_item_code;
          }
          if (offer.offer_applied) {
            offer.offer_applied == !!offer.offer_applied;
          } else {
            offer.offer_applied = false;
            if (offer.apply_type != 'Item Group') {
              offer.offer_applied = !!offer.auto;
            }
          }
          console.info('offer_applied ==> ' + offer.offer_applied);

          this.pos_offers.push(offer);
          evntBus.$emit('show_mesage', {
            text: 'New Offer Available',
            color: 'warning',
          });
        }
      });
    },
    removeOffers(offers_id_list) {
      this.pos_offers = this.pos_offers.filter(
        (offer) => !offers_id_list.includes(offer.row_id)
      );
    },
    handelOffers() {
      console.info('Trigger handelOffers');
      const applyedOffers = this.pos_offers.filter(
        (offer) => offer.offer_applied
      );
      evntBus.$emit('update_invoice_offers', applyedOffers);
    },
    handleNewLine(str) {
      if (str) {
        return str.replace(/(?:\r\n|\r|\n)/g, '<br />');
      } else {
        return '';
      }
    },
    get_give_items(offer) {
      if (offer.apply_type == 'Item Code') {
        return [offer.apply_item_code];
      } else if (offer.apply_type == 'Item Group') {
        const items = JSON.parse(localStorage.getItem('items_storage'));
        const filterd_items = items.filter(
          (item) => item.item_group == offer.apply_item_group
        );
        return filterd_items;
      } else {
        return [];
      }
    },
  },

  watch: {
    pos_offers: {
      deep: true,
      handler(pos_offers) {
        this.handelOffers();
      },
    },
  },

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
      });
    });
    evntBus.$on('update_customer', (customer) => {
      if (this.customer != customer) {
        this.offers = [];
      }
    });
    evntBus.$on('update_pos_offers', (data) => {
      this.updatePosOffers(data);
    });
  },

  destroyed() {},
};
</script>
