<template>
    <v-container fluid >
            
            <v-row class="mb-6">
                <v-col cols="8" class="grey lighten-5">
                    <ItemsSelector></ItemsSelector>
                </v-col>
                
            </v-row>
        </v-container>
</template>


<script>
        import ItemsSelector from './ItemsSelector.vue'

        export default {
                data: function () {
                        return {       
                                
                        }
                },
                components: {
                       ItemsSelector,
                },
               methods:{
                       
                },
        }
        
</script>

<style scoped>
       
        
</style>