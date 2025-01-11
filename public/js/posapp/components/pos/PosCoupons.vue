<template>
  <div>
    <v-card class="selection mx-auto bg-grey-lighten-5" style="max-height: 80vh; height: 80vh">
      <v-card-title>
        <v-row no-gutters align="center" justify="center">
          <v-col cols="6">
            <span class="text-h6 text-primary">{{ __('Coupons') }}</span>
          </v-col>
          <v-col cols="4">
            <v-text-field density="compact" variant="outlined" color="primary" :label="frappe._('Coupon')"
              bg-color="white" hide-details v-model="new_coupon" class="mr-4"></v-text-field>
          </v-col>
          <v-col cols="2">
            <v-btn class="pa-1" color="success" theme="dark" @click="add_coupon(new_coupon)">{{ __('add') }}</v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      <div class="my-0 py-0 overflow-y-auto" style="max-height: 75vh" @mouseover="style = 'cursor: pointer'">
        <v-data-table :headers="items_headers" :items="posa_coupons" :single-expand="singleExpand"
          v-model:expanded="expanded" item-key="coupon" class="elevation-1" :items-per-page="itemsPerPage"
          hide-default-footer>
          <template v-slot:item.applied="{ item }">
            <v-checkbox-btn :v-model="item.applied" disabled></v-checkbox-btn>
          </template>
        </v-data-table>
      </div>
    </v-card>

    <v-card flat style="max-height: 11vh; height: 11vh" class="cards mb-0 mt-3 py-0">
      <v-row align="start" no-gutters>
        <v-col cols="12">
          <v-btn block class="pa-1" size="large" color="warning" theme="dark" @click="back_to_invoice">{{ __('Back')
            }}</v-btn>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>

export default {
  data: () => ({
    loading: false,
    pos_profile: '',
    customer: '',
    posa_coupons: [],
    new_coupon: null,
    itemsPerPage: 1000,
    singleExpand: true,
    items_headers: [
      { title: __('Coupon'), value: 'coupon_code', align: 'start' },
      { title: __('Type'), value: 'type', align: 'start' },
      { title: __('Offer'), value: 'pos_offer', align: 'start' },
      { title: __('Applied'), value: 'applied', align: 'start' },
    ],
  }),

  computed: {
    couponsCount() {
      return this.posa_coupons.length;
    },
    appliedCouponsCount() {
      return this.posa_coupons.filter((el) => !!el.applied).length;
    },
  },

  methods: {
    back_to_invoice() {
      this.eventBus.emit('show_coupons', 'false');
    },
    add_coupon(new_coupon) {
      if (!this.customer || !new_coupon) {
        this.eventBus.emit('show_message', {
          title: __('Select a customer to use coupon'),
          color: 'error',
        });
        return;
      };
      const exist = this.posa_coupons.find(
        (el) => el.coupon_code == new_coupon
      );
      if (exist) {
        this.eventBus.emit('show_message', {
          title: __('This coupon already used !'),
          color: 'error',
        });
        return;
      }
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_pos_coupon',
        args: {
          coupon: new_coupon,
          customer: vm.customer,
          company: vm.pos_profile.company,
        },
        callback: function (r) {
          if (r.message) {
            const res = r.message;
            if (res.msg != 'Apply' || !res.coupon) {
              vm.eventBus.emit('show_message', {
                text: res.msg,
                color: 'error',
              });
            } else {
              vm.new_coupon = null;
              const coupon = res.coupon;
              vm.posa_coupons.push({
                coupon: coupon.name,
                coupon_code: coupon.coupon_code,
                type: coupon.coupon_type,
                applied: 0,
                pos_offer: coupon.pos_offer,
                customer: coupon.customer || vm.customer,
              });
            }
          }
        },
      });
    },
    setActiveGiftCoupons() {
      if (!this.customer) return;
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_active_gift_coupons',
        args: {
          customer: vm.customer,
          company: vm.pos_profile.company,
        },
        callback: function (r) {
          if (r.message) {
            const coupons = r.message;
            coupons.forEach((coupon_code) => {
              vm.add_coupon(coupon_code);
            });
          }
        },
      });
    },

    updatePosCoupons(offers) {
      this.posa_coupons.forEach((coupon) => {
        const offer = offers.find(
          (el) => el.offer_applied && el.coupon == coupon.coupon
        );
        if (offer) {
          coupon.applied = 1;
        } else {
          coupon.applied = 0;
        }
      });
    },

    removeCoupon(reomove_list) {
      this.posa_coupons = this.posa_coupons.filter(
        (coupon) => !reomove_list.includes(coupon.coupon)
      );
    },
    updateInvoice() {
      this.eventBus.emit('update_invoice_coupons', this.posa_coupons);
    },
    updateCounters() {
      this.eventBus.emit('update_coupons_counters', {
        couponsCount: this.couponsCount,
        appliedCouponsCount: this.appliedCouponsCount,
      });
    },
  },

  watch: {
    posa_coupons: {
      deep: true,
      handler() {
        this.updateInvoice();
        this.updateCounters();
      },
    },
  },

  created: function () {
    this.$nextTick(function () {
      this.eventBus.on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
      });
    });
    this.eventBus.on('update_customer', (customer) => {
      if (this.customer != customer) {
        const to_remove = [];
        this.posa_coupons.forEach((el) => {
          if (el.type == 'Promotional') {
            el.customer = customer;
          } else {
            to_remove.push(el.coupon);
          }
        });
        this.customer = customer;
        if (to_remove.length) {
          this.removeCoupon(to_remove);
        }
      }
      this.setActiveGiftCoupons();
    });
    this.eventBus.on('update_pos_coupons', (data) => {
      this.updatePosCoupons(data);
    });
    this.eventBus.on('set_pos_coupons', (data) => {
      this.posa_coupons = data;
    });
  },
};
</script>
