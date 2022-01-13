<template>
  <v-row justify="center">
    <v-dialog v-model="quantityDialog" max-width="600px">
      <v-card min-height="200px">
        <v-card-title>
          <!-- <span class="headline indigo--text">Add Quantity</span> -->
		  <span class="headline indigo--text">{{__('Select Return Invoice')}}</span>
          <v-spacer></v-spacer>
        </v-card-title>
		<v-container>
          <v-row class="mb-4">
			<v-text-field
					dense
					outlined
					autofocus
					clearable
					color="indigo"
					:label="frappe._('QTY')"
					background-color="white"
					hide-details
					class="mx-4"
					v-model.number="item.qty"
					type="number"
					@keydown.enter="search_by_enter"
			></v-text-field>
          </v-row>
        </v-container>
		<v-card-actions class="mt-4">
          <v-spacer></v-spacer>
		  <v-btn color="error" dark @click="close_dialog">Close</v-btn>
          <v-btn color="success mx-2" dark @click="add_item(item)">{{__('Continue')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    quantityDialog: false,
    item: null
  }),
  methods: {
    close_dialog() {
      this.quantityDialog = false;
    },
	search_by_enter(e) {
      if (e.keyCode === 13) {
        evntBus.$emit('add_item', this.item);
		this.close_dialog();
      }
    },
    add_item(item) {
      evntBus.$emit('add_item', item);
      this.close_dialog();
    },
  },
  created: function () {
    evntBus.$on('open_quantity_model', (item) => {
		console.log('<><><><><><', item)
      this.quantityDialog = true;
      this.item = item || null;
    });
  },
};
</script>