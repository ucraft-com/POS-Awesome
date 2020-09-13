<template>
<v-app>
<div class="container1">
<v-main>
        <Navbar @changePage="setPage($event)"> </Navbar>  
        <h1>Hello Pos Awseome</h1>
        <keep-alive>
                <component v-bind:is="page" class="mx-4 md-4"></component>
        </keep-alive>
</v-main>
</div>
</v-app>
</template>

<script>
        import Navbar from './components/Navbar.vue'
        import POS from './components/pos/Pos.vue'

        export default {
                name: "TableRoot",
                data: function () {
                        return {       
                                page : "POS",
                        }
                },
                components: {
                       Navbar,
                       POS
                },
               methods:{
                        setPage (page) {
                                this.page = page;
                        },
                },
        }
        
</script>

<style scoped>
        .container1 {
                margin-top: 0px;
        }
        
</style>