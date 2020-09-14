<template>
        <div fluid >
            <v-row>
                <v-col cols="8" class="pos pr-0">
                    <ItemsSelector></ItemsSelector>
                </v-col>
                 <v-col cols="4" class="pos">
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