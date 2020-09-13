<template>
    <nav>
        <v-app-bar flat height="40">
            <v-app-bar-nav-icon @click.stop="mini = !mini" class="grey--text"></v-app-bar-nav-icon>
            <v-toolbar-title class="text-uppercase indigo--text">
                <span class="font-weight-light">pos</span>
                <span>awesome</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>
            
            <div class="text-center">
                <v-menu offset-y open-on-hover>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                    color="grey"
                    dark
                    text
                    v-bind="attrs"
                    v-on="on"
                    >
                    Pages
                    </v-btn>
                </template>
                <v-card
                    class="mx-auto"
                    max-width="300"
                    tile
                >
                    <v-list dense>
                        <v-list-item-group v-model="item" color="primary">
                            <v-list-item
                                v-for="(item, index) in items"
                                :key="item.text"
                                @click="[changePage(item.text), item = index]"
                            >
                                <v-list-item-icon>
                                    <v-icon v-text="item.icon"></v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                    <v-list-item-title v-text="item.text"></v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list-item-group>
                    </v-list>
                 </v-card>
                </v-menu>
            </div>
            <v-btn text color="grey" @click="go_to">
                <v-icon>mdi-home</v-icon>
                <span right>Home</span>
            </v-btn>
        </v-app-bar>
        <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" app class="indigo margen-top">
                <v-list dark>
                <v-list-item class="px-2">
                    <v-list-item-avatar>
                    <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
                    </v-list-item-avatar>

                    <v-list-item-title>John Leider</v-list-item-title>

                    <v-btn
                    icon
                    @click.stop="mini = !mini"
                    >
                    <v-icon>mdi-chevron-left</v-icon>
                    </v-btn>
                </v-list-item>
                <!-- <MyPopup/> -->
                <v-list-item-group v-model="item" color="white">
                    <v-list-item
                    v-for="item in items"
                    :key="item.text"
                    @click="changePage(item.text)"
                    >
                        <v-list-item-icon>
                            <v-icon v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title v-text="item.text"></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
                </v-list>
        </v-navigation-drawer>
    </nav>
</template>

<script>

// import MyPopup from './MyPopup.vue';

export default {
    // components: {MyPopup},
    data(){
        return {
            drawer: true,
            mini: true,
            item: 0,
            items: [
                { text: 'POS', icon: 'mdi-point-of-sale' },
                { text: 'Dashboard', icon: 'mdi-view-dashboard' },
                { text: 'Projects', icon: 'mdi-folder-open' },
                { text: 'Team', icon: 'mdi-account-box-multiple' },
            ],
            page: "",
            fav: true,
            menu: false,
            message: false,
            hints: true,
        }
    },
    methods:{
            changePage(key){
                this.$emit('changePage', key);
            },
            go_to(){
                //  window.location = document.location.href.substring(0,document.location.href.length - 6);
                frappe.set_route('workspace', 'home')
                location.reload();
            },
        },
}
</script>

<style scoped>
        .margen-top {
                margin-top: 0px;
        }
        
</style>