<template>
<v-app>
<div class="container1">
<v-main>
        <!-- <navbar @changePage="setPage($event)" > </navbar>   -->
        <Navbar> </Navbar>  
        <keep-alive>
        <!-- <component v-bind:is="page" class="mx-4 md-4"></component> -->
        <h1>Hello Pos Awseome</h1>
        </keep-alive>
</v-main>
</div>
</v-app>
</template>

<script>
        import Navbar from './components/Navbar.vue'

        export default {
                name: "TableRoot",
                data: function () {
                        return {       
                                page : "Home",
                        }
                },
                components: {
                       Navbar,
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