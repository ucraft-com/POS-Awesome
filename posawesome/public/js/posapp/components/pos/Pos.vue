<template>
  <div fluid>
    <ClosingDialog></ClosingDialog>
    <Drafts></Drafts>
    <NewCustomer></NewCustomer>
    <OpeningDialog v-if="dialog" :dialog="dialog"></OpeningDialog>
    <v-row v-show="!dialog">
      <v-col v-show="!payment" xl="5" lg="6" md="6" sm="6" cols="12" class="pos pr-0">
        <ItemsSelector></ItemsSelector>
      </v-col>
      <v-col v-show="payment" xl="5" lg="6" md="6" sm="6" cols="12" class="pos pr-0">
        <Payments></Payments>
      </v-col>
      <v-col xl="7" lg="6" md="6" sm="6" cols="12" class="pos">
        <Invoice></Invoice>
      </v-col>
    </v-row>
  </div>
</template>


<script>
import { evntBus } from "../../bus";
import ItemsSelector from "./ItemsSelector.vue";
import Invoice from "./Invoice.vue";
import OpeningDialog from "./OpeningDialog.vue";
import Payments from "./Payments.vue";
import Drafts from "./Drafts.vue";
import ClosingDialog from "./ClosingDialog.vue";
import NewCustomer from "./NewCustomer.vue";

export default {
  data: function () {
    return {
      dialog: false,
      pos_profile: "",
      pos_opening_shift: "",
      payment: false,
    };
  },

  components: {
    ItemsSelector,
    Invoice,
    OpeningDialog,
    Payments,
    Drafts,
    ClosingDialog,
    NewCustomer,
  },

  methods: {
    check_opening_entry() {
      return frappe
        .call("posawesome.posawesome.api.posapp.check_opening_shift", {
          user: frappe.session.user,
        })
        .then((r) => {
          if (r.message) {
            this.pos_profile = r.message.pos_profile;
            this.pos_opening_shift = r.message.pos_opening_shift;
            evntBus.$emit("register_pos_profile", r.message);
            evntBus.$emit("set_company", r.message.company);
            console.log("LoadPosProfile");
          } else {
            this.create_opening_voucher();
          }
        });
    },
    create_opening_voucher() {
      this.dialog = true;
    },
     get_closing_data() {
      return frappe
        .call("posawesome.posawesome.doctype.pos_closing_shift.pos_closing_shift.make_closing_shift_from_opening", {
          opening_shift: this.pos_opening_shift,
        })
        .then((r) => {
          if (r.message) {
            evntBus.$emit("open_ClosingDialog",r.message);
          } else {
            console.log(r)
          }
        });
    },
    submit_closing_pos(data){
      frappe
        .call("posawesome.posawesome.doctype.pos_closing_shift.pos_closing_shift.submit_closing_shift", {
          closing_shift: data,
        })
        .then((r) => {
          if (r.message) {
            evntBus.$emit("show_mesage", {
              text: `POS Shift Closed`,
              color: "success",
            });
            this.check_opening_entry()
          } else {
            console.log(r)
          }
        });
    },
  },

  created: function () {
    this.$nextTick(function () {
      this.check_opening_entry();
      evntBus.$on("close_opening_dialog", () => {
        this.dialog = false;
      });
      evntBus.$on("register_pos_data", (data) => {
        this.pos_profile = data.pos_profile;
        this.pos_opening_shift = data.pos_opening_shift;
        evntBus.$emit("register_pos_profile", data);
        console.log("LoadPosProfile");
      });
      evntBus.$on("show_payment", (data) => {
        this.payment = true ? data ==="true": false;
        // evntBus.$emit("update_cur_items_details");
      })
      evntBus.$on("open_closing_dialog", () => {
        this.get_closing_data()
      })
      evntBus.$on("submit_closing_pos", (data) => {
        this.submit_closing_pos(data)
      })
    });
  },
};
</script> 

<style scoped>
</style>