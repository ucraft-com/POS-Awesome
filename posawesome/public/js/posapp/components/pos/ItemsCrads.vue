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
                    <v-btn icon color="red" @click.stop="remove_item(item.item_code)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-list-item-action>
                <v-list-item-content class="py-0">
                        <v-row align="center"  class="ma-0">
                            <v-col la="4" md="4" sm="12" cols="12" class="pa-1">
                                <div v-text="item.item_name"></div>
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
                                <div align="center" v-text="item.qty * item.price"></div>
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
<v-row>
    <v-col class="pt-0 pr-0" cols="8">
        <v-card style="max-height: 20vh; height: 20vh" class="cards mb-0 mt-3 py-0 grey lighten-5">
            <v-row no-gutters class="pa-1 pt-2" style="height: 100%">
                <v-col cols="6" no-gutters>
                    <v-row  no-gutters class="ma-1 pa-0" style="height: 100%">
                        <v-col cols="12">
                            <v-text-field
                                v-model="total_qty"
                                label="Total Qty"
                                outlined
                                dense
                                readonly
                                hide-details
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="subtotal"
                                label="Subtotal"
                                outlined
                                dense
                                readonly
                                hide-details
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="items_discount"
                                label="Items Discount"
                                outlined
                                dense
                                readonly
                                hide-details
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col no-gutters cols="6">
                    <v-row no-gutters class="ma-1 pa-0" style="height: 100%">
                        <v-col cols="12">
                            <v-text-field
                                v-model="additional_discount"
                                label="ِAdditional Discount"
                                outlined
                                dense
                                
                                hide-details
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="total_tax"
                                label="TAX"
                                outlined
                                dense
                                readonly
                                hide-details
                            ></v-text-field>
                        </v-col>
                        <v-col  cols="12">
                            <v-text-field
                                v-model="total"
                                label="Total"
                                outlined
                                dense
                                readonly
                                hide-details
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
                
        </v-card>
    </v-col>
    <v-col class="pt-0 pr-3" cols="4">
        <v-card flat style="max-height: 20vh; height: 20vh" class="cards mb-0 mt-3 py-0">
                <v-row align="start" style="height: 53%">
                    <v-col cols="12">
                        <v-btn block class="pa-0" large color="warning" dark>Get Hold Invoice</v-btn>
                    </v-col >
                    <v-col cols="6">
                        <v-btn block class="pa-0" large color="error" dark>Cancel</v-btn>
                    </v-col >
                    <v-col cols="6">
                        <v-btn block class="pa-0" large color="success" dark>New</v-btn>
                    </v-col>
                </v-row>
                <v-row align="end" style="height: 54%">
                    <v-col cols="12">
                        <v-btn block class="pa-0" large color="primary" dark>PAY</v-btn>
                    </v-col>
                </v-row> 
        </v-card>
    </v-col>
</v-row>
</div>
</template>

<script>
import Customer from './Customer.vue'
export default {
    props: [
            "items"
    ],
    data() {
        return {
            total_qty: 0,
            subtotal: 0,
            items_discount: 0,
            additional_discount: 0,
            total_tax: 0,
            total: 0,
        }
        
    },
    components: {
        Customer,
    },
    computed: {
       
    },
    methods: {
        sortBy(prop) {
            this.projects.sort((a,b) => a[prop] < b[prop] ? -1 : 1)
        },
        remove_item(value) {
            console.log(value)
            // this.items = this.items.filter(function(el) { return el != value; }); 
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