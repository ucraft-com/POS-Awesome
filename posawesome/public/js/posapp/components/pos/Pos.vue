<template>
        <div fluid >
            <v-row>
                <v-col xl="6" lg="5" md="5" sm="6" cols="12"  class="pos pr-0">
                    <ItemsSelector></ItemsSelector>
                </v-col>
                 <v-col  xl="6" lg="7" md="7" sm="6" cols="12" class="pos">
                    <ItemsCrads></ItemsCrads>
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
                                
                        }
                },
                components: {
                       ItemsSelector,
                       ItemsCrads,
                },
               methods:{
                       
                },
        }
        
</script>

<style scoped>
       
        
</style>