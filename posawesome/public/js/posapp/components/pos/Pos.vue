<template>
  <div fluid>
    <OpeningDialog v-if="dialog" :dialog="dialog"></OpeningDialog>
    <v-row v-show="!dialog">
      <v-col xl="5" lg="6" md="6" sm="6" cols="12" class="pos pr-0">
        <ItemsSelector></ItemsSelector>
      </v-col>
      <v-col xl="7" lg="6" md="6" sm="6" cols="12" class="pos">
        <ItemsCrads></ItemsCrads>
      </v-col>
    </v-row>
  </div>
</template>


<script>
import { evntBus } from "../../bus";
import ItemsSelector from "./ItemsSelector.vue";
import ItemsCrads from "./ItemsCrads.vue";
import OpeningDialog from "./OpeningDialog.vue";

export default {
  data: function () {
    return {
      dialog: false,
      pos_profile: "",
      pos_opening_shift: "",
    };
  },

  components: {
    ItemsSelector,
    ItemsCrads,
    OpeningDialog,
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
            console.log("LoadPosProfile")
          } else {
            this.create_opening_voucher();
          }
        });
      // frappe.call({
      //   method: "posawesome.posawesome.api.posapp.check_opening_shift",
      //   args: { user: frappe.session.user },
      //   async: false,
      //   callback: function (r) {
      //     if (r.message) {
      //       if (r.message) {
      //         this.pos_profile = r.message.pos_profile;
      //         this.pos_opening_shift = r.message.pos_opening_shift;
      //         evntBus.$emit("update_items", r.message.pos_profile);
      //       } else {
      //         this.create_opening_voucher();
      //       }
      //     }
      //   },
      // });
    },
    create_opening_voucher() {
      console.log("create_opening_voucher");
      this.dialog = true;
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
        console.log("LoadPosProfile")
      });
    });
  },
};
</script>

<style scoped>
</style>