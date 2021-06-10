<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5"
      style="max-height: 85vh; height: 85vh"
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
                v-model="item.offer_applied"
              ></v-simple-checkbox>
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
        <!-- <v-col cols="12">
          <v-btn block class="mt-2" large color="primary" dark @click="submit"
            >Submit Payments</v-btn
          >
        </v-col> -->
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
      // { text: 'Item Code', value: 'item_code', align: 'start' },
      { text: 'Apply On', value: 'apply_on', align: 'start' },
      { text: 'Offer', value: 'offer', align: 'start' },
      { text: 'Applied', value: 'offer_applied', align: 'start' },
    ],
  }),

  methods: {
    back_to_invoice() {
      evntBus.$emit('show_offers', 'false');
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
          offer.row_id = this.makeid(20);
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
  },

  computed: {},

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

  watch: {},
};
</script>
