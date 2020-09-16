<template>
<div>
<v-card style="max-height: 70vh; height: 70vh" class="cards my-0 py-0 grey lighten-5">
     <Customer></Customer>
    <v-list class="my-0 py-0 overflow-y-auto" style="max-height: 57vh">
      <v-list-group
       v-for="(item, index) in items"
       :key="index"
        v-model="item.active"
        :prepend-icon="item.action"
        color="primary"
        class="my-0 py-0 border_line_bottom"
      >
        <template v-slot:activator class="pa-0">
          <v-list-item :key="item.item_code" class="px-0">
            <template>
                <v-list-item-action class="pa-0 mr-2 my-0">
                    <v-btn icon color="red" @click.stop="out_console(item.item_code)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-list-item-action>
                <v-list-item-content class="py-0">
                        <v-row align="center"  class="ma-0">
                            <v-col la="4" md="4" sm="12" cols="12" class="pa-1">
                                <div v-text="item.item_code"></div>
                            </v-col>
                            <v-col align="center" cols="1" class="pa-1">
                                <v-btn icon small color="indigo lighten-1" @click.stop="">
                                    <v-icon>mdi-minus-circle-outline</v-icon>
                                </v-btn>
                            </v-col>
                            <v-col la="2" md="2" sm="3" cols="3" class="pa-1 text-overline">
                                <div align="center"  v-text="item.qty"></div>
                            </v-col>
                            <v-col align="center" cols="1" class="pa-1">
                                <v-btn icon small  color="indigo lighten-1" @click.stop="">
                                    <v-icon>mdi-plus-circle-outline</v-icon>
                                </v-btn>
                            </v-col>
                            <v-col la="2" md="2" sm="3" cols="3" class="pa-1 text-overline">
                                <div align="center" v-text="item.price"></div>
                            </v-col>
                            <v-col la="2" md="2" sm="4" cols="3" class="pa-1 text-overline">
                                <div align="center" v-text="item.total"></div>
                            </v-col>
                        </v-row>
                </v-list-item-content>
            
            </template>
          </v-list-item>
        </template>
            <v-card flat color="blue lighten-5">
                <v-card-text>Some info</v-card-text>
            </v-card>
        
      </v-list-group>
    </v-list>
</v-card>
<v-card style="max-height: 20vh; height: 20vh" class="cards mb-0 mt-3 py-0 grey lighten-5">
        <div>some botns</div>
</v-card>
</div>
</template>

<script>
import Customer from './Customer.vue'
export default {
    data() {
        return {
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
                    active: true,
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
                {
                    item_code: "Pepsi 200 ml",
                    qty: '5',
                    vat: '18',
                    price: '3.6',
                    total: '12,33',
                    active: true,
                },
                {
                    item_code: "Pepsi 330 ml Kutu Kola",
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

<style scoped>
    .border_line_bottom{
        border-bottom: 1px solid lightgray;
    }
</style>