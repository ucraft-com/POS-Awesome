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
          label="Serch"
          hint="Search by item code, serial number, batch no or barcode"
          background-color="white"
          hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12"  class="pt-0 mt-0">
              <div fluid  class="items">
                <v-row dense class="overflow-y-auto" style="max-height: 68vh">
                  <v-col
                    v-for="(card, idx) in cards"
                    :key="idx"
                    xl="2" lg="3" md="6" sm="6" cols="6"
                  >
                    <v-card hover="hover">
                      <v-img
                        :src="card.src"
                        class="white--text align-end"
                        gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
                        height="100px"
                      >
                      <v-card-text v-text="card.title" class="text-subtitle-2 px-1 pb-2"></v-card-text>
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
  export default {
    data: () => ({
      items_view: 'card',
      item_group: 'Fizz',
      favourites_view: false,
      items_group: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      cards: [
        { title: 'Pepsi 330 ml Kutu Kola', src: 'https://cdn.cimri.io/image/1000x1000/pepsimlkutukola_150033727.jpg', flex: 2 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 2 },
        { title: 'Coca Cola Gazlı İçecek Kola 1.25 L', src: 'https://ayb.akinoncdn.com/products/2019/01/18/1796/b792f041-5479-4d5f-a74e-233d5da474bc.jpg', flex: 2 },
        { title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 2 },
        { title: 'COCA COLA Coca Cola Kutu 200 Ml', src: 'https://cdnd.bizimtoptan.com.tr/product/480x480/f73e3_COCA_COLA_KUTU_200_ML.jpg', flex: 2 },
        { title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 2 },
        { title: 'Favorite road trips', src: 'https://m.media-amazon.com/images/I/41GbUGRBhOL._AC_SS350_.jpg', flex: 2 },
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 2 },
        { title: 'Pre-fab homes', src: 'https://ayb.akinoncdn.com/products/2019/01/23/1998/18958675-db88-4a79-a108-f95b1a6522e9_size780x780_quality60_cropCenter.jpg', flex: 2 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 2 },
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 2 },
        { title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 2 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 2 },
        { title: 'Best airlines', src: '', flex: 2 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 2 },
      ],
    }),
  }
</script>

<style scoped>

</style>