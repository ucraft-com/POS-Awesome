<!-- <template>
  <div>
    <v-card class="cards mb-0 mt-3 py-0 grey lighten-5">
      <v-row no-gutters>
        <v-col cols="5">
          <v-row no-gutters class="pa-1 pt-2 pl-0">
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="info"
                dark
                @click="get_draft_orders"
                >{{ __("Select Sales Order") }}</v-btn
              >
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { evntBus } from "../../bus";
import format from "../../format";
import Customer from "./Customer.vue";

export default {
  methods: {
    get_draft_orders() {
      const vm = this;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.get_draft_orders",
        args: {
        //   pos_opening_shift: this.pos_opening_shift.name,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            evntBus.$emit("open_orders", r.message);
          }
        },
      });
    },
  },
};
</script> -->
