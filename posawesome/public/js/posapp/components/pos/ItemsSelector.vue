<template>
  <div>
      <v-card class="selection mx-auto grey lighten-5" style="max-height: 80vh; height: 80vh">
      <v-row class="items px-2 py-1">
        <v-col cols="12"  class="pb-0 mb-2">
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
          ></v-text-field>
        </v-col>
        <v-col cols="12"  class="pt-0 mt-0">
              <div fluid  class="items">
                <v-row dense class="overflow-y-auto" style="max-height: 68vh">
                  <v-col
                    v-for="(item, idx) in items"
                    :key="idx"
                    xl="2" lg="3" md="6" sm="6" cols="6"
                  >
                    <v-card hover="hover" @click="add_item(item)">
                      <v-img
                        :src="item.image"
                        class="white--text align-end"
                        gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
                        height="100px"
                      >
                      <v-card-text v-text="item.item_name" class="text-subtitle-2 px-1 pb-2"></v-card-text>
                      <!-- <v-card-subtitle v-text="card.name" class="pb-0"></v-card-subtitle> -->
                      </v-img>
                      <v-card-text class="text--primary pa-1">
                        <div class="text-caption indigo--text accent-3">$ 50.00</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
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
          <v-btn-toggle
          v-model="items_view"
          color="primary accent-3"
          group
          dense
          rounded
          >
          <v-btn value="card">
            Card View
          </v-btn>
          <v-btn value="list">
            List View
          </v-btn>
        </v-btn-toggle>
        </v-col>
        <v-col cols="4" class="mt-1">
        <v-btn-toggle
          v-model="favourites_view"
          color="success accent-3"
          group
          dense
          rounded
          >
        <v-btn value="True">
            Favourites
          </v-btn>
        </v-btn-toggle>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>


<script>
  import { evntBus } from "../../bus";
  export default {
    data: () => ({
      items_view: 'card',
      item_group: 'Fizz',
      favourites_view: false,
      items_group: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      items: [],
    }),

    methods: {
        get_items() {
          const vm = this;
          frappe.call({
              method: 'posawesome.posawesome.page.posapp.posapp.get_items',
              args: {

              },
              callback: function(r) {
                  if (r.message) {
                      // console.log(r.message);
                      vm.items = r.message;
                  }
              }
          });
        },
        add_item(item){
          evntBus.$emit('add_item', item);
        }
    },

    created: function () {
        this.$nextTick(function () {
          this.get_items();
        });
        
    }

  }

  
</script>

<style scoped>

</style>