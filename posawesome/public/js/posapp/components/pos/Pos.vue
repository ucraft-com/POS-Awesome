<template>
        <div fluid>
            <v-row>
                <v-col xl="6" lg="5" md="5" sm="6" cols="12"  class="pos pr-0">
                    <ItemsSelector @add_item="add_item($event)"></ItemsSelector>
                </v-col>
                 <v-col  xl="6" lg="7" md="7" sm="6" cols="12" class="pos">
                    <ItemsCrads :items="items"></ItemsCrads>
                </v-col>
            </v-row>
        </div>
</template>


<script>
        import ItemsSelector from './ItemsSelector.vue'
        import ItemsCrads from "./ItemsCrads.vue";

        export default {
                data: function () {
                        return {       
                                items: [],
                        }
                },
                components: {
                       ItemsSelector,
                       ItemsCrads,
                },
               methods:{
                       add_item(item){
                                item.qty = 1;
                                item.vat = 18;
                                item.price = 25;
                                item.total = 30;
                                item.active = false,
                                this.items.unshift(item)
                       },
                },
        }
        
</script>

<style scoped>
       
        
</style>