<template>
        <div fluid >
            
            <v-row>
                <v-col cols="8" class="pos">
                    <ItemsSelector></ItemsSelector>
                </v-col>

            </v-row>
        </div>
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