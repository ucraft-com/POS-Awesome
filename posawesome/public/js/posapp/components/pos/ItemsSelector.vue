<template>
      <v-card class="selection mx-auto grey lighten-5" style="max-height: 90vh; height: 90vh">
      <v-row class="items px-2 py-1">
        <v-col cols="12"  class="pb-0 mb-0">
          <v-text-field 
          dense 
          clearable 
          autofocus 
          outlined 
          color="indigo"
          label="Serch"
          hint="Search by item code, serial number, batch no or barcode"
          background-color="white"
          ></v-text-field>
        </v-col>
    
        <v-col cols="12"  class="pt-0 mt-0">
              <div fluid  class="items">
                <v-row dense class="overflow-y-auto" style="max-height: 79vh">
                  <v-col
                    v-for="(card, idx) in cards"
                    :key="idx"
                    xl="2" lg="3" md=4 sm="6" cols="12"
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
</template>


<script>
  export default {
    data: () => ({
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
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 2 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 2 },
      ],
    }),
  }
</script>

<style scoped>

</style>