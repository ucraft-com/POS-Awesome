<template>
<v-card style="max-height: 90vh; height: 90vh" class="cards my-0 py-0">
     <Customer></Customer>
    <v-list class="my-0 py-0">
      <v-list-item-group
        v-model="selected"
        color="primary"
        class="my-0 py-0"
      >
        <template v-for="(item, index) in items">
          <v-list-item :key="item.item_code" class="px-1">
            <template v-slot:default="{ active, toggle }">
                <v-list-item-action class="pa-0 mr-2 my-0">
                    <v-btn icon color="red" @click="out_console(item.item_code)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-list-item-action>
              <v-list-item-content class="py-0">
                    <v-row align="center"  class="ma-0">
                        <v-col cols="4" class="pa-1">
                             <div v-text="item.item_code"></div>
                        </v-col>
                        <v-col cols="1" class="pa-1">
                            <v-btn icon small color="green">
                                <v-icon>mdi-minus-box-outline</v-icon>
                            </v-btn>
                        </v-col>
                        <v-col cols="2" class="pa-1 text-overline">
                            <div align="center"  v-text="item.qty"></div>
                        </v-col>
                        <v-col cols="1" class="pa-1">
                            <v-btn icon small  color="green">
                                <v-icon>mdi-plus-box-outline</v-icon>
                            </v-btn>
                        </v-col>
                        <v-col cols="2" class="pa-1 text-overline">
                            <div align="center" v-text="item.price"></div>
                        </v-col>
                        <v-col cols="2" class="pa-1 text-overline">
                            <div align="center" v-text="item.total"></div>
                        </v-col>
                    </v-row>
              </v-list-item-content>
              <v-list-item-action class=" py-0 my-0">
                <v-icon
                  v-if="!active"
                  color="grey lighten-1"
                >
                  mdi-star
                </v-icon>

                <v-icon
                  v-else
                  color="yellow"
                >
                  mdi-star
                </v-icon>
              </v-list-item-action>
            </template>
          </v-list-item>

          <v-divider class="my-0 py-0"
            v-if="index + 1 < items.length"
            :key="index"
          ></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
</v-card>
</template>

<script>
import Customer from './Customer.vue'
export default {
    data() {
        return {
            selected: 0,
            items: [
                {
                    item_code: "Pepsi 200 ml",
                    qty: '5',
                    vat: '18',
                    price: '3.6',
                    total: '12,33',
                },
                {
                    item_code: "Pepsi 330 ml Kutu Kola",
                    qty: '2',
                    vat: '18',
                    price: '3',
                    total: '6',
                },
                {
                    item_code: "Favorite road trips",
                    qty: '2',
                    vat: '18',
                    price: '3',
                    total: '6',
                },
                {
                    item_code: "Coca Cola Gazlı İçecek Kola 1.25 L",
                    qty: '100',
                    vat: '18',
                    price: '123.99',
                    total: '1231.23',
                },
                {
                    item_code: "COCA COLA Coca Cola Kutu 200 Ml",
                    qty: '2',
                    vat: '18',
                    price: '3',
                    total: '6',
                },
            ],
        }
    },
    components: {
        Customer,
    },
    methods: {
        sortBy(prop) {
            this.projects.sort((a,b) => a[prop] < b[prop] ? -1 : 1)
        },
        out_console(value) {
            console.log(value)
        }
    },
    mounted: function () {
        // this.$nextTick(function () {
        // const vm = this;
        //     frappe.call({
        //         method: 'roxtools.roxtools.doctype.myprojects.myprojects.get_all_projects',
        //         async: false,
        //         callback: function(r) {
        //             if (r.message) {
        //                 // console.log(r.message);
        //                 vm.projects = r.message;
        //             }
        //         }
        //     });
        // })
        // this.$nextTick(function () {
        //     const vm = this;
        //     frappe.realtime.on('rox_add_project', function(data) {
        //         vm.projects.push(data);
        //     });
        // })
    }
}
</script>