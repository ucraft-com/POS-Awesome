<template>
<v-card class="cards mx-auto grey lighten-5" style="max-height: 90vh; height: 90vh">
     <Customer></Customer>
    <v-expansion-panels
            hover="hover"
            class="px-2"
            >
        <v-expansion-panel
            v-for="project in projects"
            :key="project.name"
            >
            <v-expansion-panel-header class="pl-2">{{ project.title }}</v-expansion-panel-header>
            <v-expansion-panel-content class="px-1">
                <v-row>
                    <v-col cols="4">
                        <div class="px-0 font-weight-bold">{{ project.person }}</div>
                    </v-col>
                    <v-col cols="4">
                        <div class="px-0">{{ project.due }}</div>
                    </v-col>
                        <v-col cols="">
                        <div class="px-0">{{ project.status }}</div>
                    </v-col>
                </v-row>
                <div class="px-0 grey--text">{{ project.content }}</div>
                
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</v-card>
</template>

<script>
import Customer from './Customer.vue'
export default {
    data() {
        return {
             projects: [
                { title: 'Design 1 a new website', person: 'The Net Ninja', due: '1st Jan 2019', status: 'ongoing', content: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt consequuntur eos eligendi illum minima adipisci deleniti, dicta mollitia enim explicabo fugiat quidem ducimus praesentium voluptates porro molestias non sequi animi!'},
                { title: 'Code up the homepage', person: 'Chun Li', due: '10th Jan 2019', status: 'complete', content: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt consequuntur eos eligendi illum minima adipisci deleniti, dicta mollitia enim explicabo fugiat quidem ducimus praesentium voluptates porro molestias non sequi animi!'},
                { title: 'Design 2 video thumbnails', person: 'Ryu', due: '20th Dec 2018', status: 'complete', content: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt consequuntur eos eligendi illum minima adipisci deleniti, dicta mollitia enim explicabo fugiat quidem ducimus praesentium voluptates porro molestias non sequi animi!'},
                { title: 'Create a 3 community forum', person: 'Gouken', due: '20th Oct 2018', status: 'overdue', content: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt consequuntur eos eligendi illum minima adipisci deleniti, dicta mollitia enim explicabo fugiat quidem ducimus praesentium voluptates porro molestias non sequi animi!'},
            ]
        }
    },
    components: {
        Customer,
    },
    methods: {
        sortBy(prop) {
            this.projects.sort((a,b) => a[prop] < b[prop] ? -1 : 1)
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