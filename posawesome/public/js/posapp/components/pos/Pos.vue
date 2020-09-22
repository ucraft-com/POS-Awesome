<template>
  <div fluid>
    <OpeningDialog :dialog=dialog></OpeningDialog>
    <v-row>
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
      shift_is_open: false,
      dialog: false,
    };
  },

  components: {
    ItemsSelector,
    ItemsCrads,
    OpeningDialog,
  },

  methods: {
    check_opening_entry() {
      // const vm = this
      return frappe
        .call(
          "posawesome.posawesome.api.posapp.check_opening_shift",
          { user: frappe.session.user }
        )
        .then((r) => {
          console.log(r.message)
          if (r.message.length) {
            // NOTE : assuming only one opening voucher is available for the current user
            // TODO : should Rendering pos
            // this.prepare_app_defaults(r.message[0]);
            console.log(r.message)
          } else {
            // TODO : should Rendering opninig shift dialog
            this.create_opening_voucher();
          }
        });
    },
    create_opening_voucher() {
      console.log("create_opening_voucher")
      this.dialog = true
    },
  },

  created: function () {
    this.$nextTick(function () {
      this.check_opening_entry();
      evntBus.$on("close_opening_dialog", () => {
      this.dialog = false;
      });

    });
  },

};
</script>

<style scoped>
</style>