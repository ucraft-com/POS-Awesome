<template>
  <v-app class="container1">
    <v-main>
      <!-- Show preloader if isLoading is true -->
      <div v-if="isLoading" class="preloader">
        <!-- Use a loading spinner icon -->
        <i class=""></i>
      </div>

      <Navbar @changePage="setPage($event)"></Navbar>
      <keep-alive>
        <component v-bind:is="page" class="mx-4 md-4"></component>
      </keep-alive>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar.vue';
import POS from './components/pos/Pos.vue';
import { evntBus } from './bus';

export default {
  data() {
    return {
      page: 'POS',
      isLoading: false, // Track whether to show preloader or not
    };
  },
  components: {
    Navbar,
    POS,
  },
  methods: {
    setPage(page) {
      this.page = page;
    },
    remove_frappe_nav() {
      // Remove Frappe navigation elements
      this.$nextTick(function () {
        $('.page-head').remove();
        $('.navbar.navbar-default.navbar-fixed-top').remove();
      });
    },
    // Method to show preloader
    showPreloader(data) {
      return this.isLoading = data;
    },
    // Method to hide preloader
    hidePreloader() {
     return this.isLoading = false;
    },
  },
  mounted() {
     
    this.showPreloader(true)
    // Remove Frappe navigation elements
    this.remove_frappe_nav();
  },
  created() {
    setTimeout(() => {
      // Remove Frappe navigation elements after a delay
      this.remove_frappe_nav();
    }, 1000);

    evntBus.$on('register_pos_profile', (data) => {
          return  this.hidePreloader();
        });

    evntBus.$on('show_loader', (data) => {
      setTimeout(() => {
          return this.showPreloader(JSON.parse(data))
        }, 10);

      });
  },
};
</script>

<style scoped>
.container1 {
  margin-top: 0px;
}
.preloader {
  /* Style your preloader here */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure it's above other content */
}

.preloader i {
  font-size: 48px; /* Adjust the size of the spinner */
  border-radius: 50%; /* Make the spinner rounded */
  border: 5px solid #333; /* Add a border for the spinner */
  border-top: 5px solid #fff; /* Change the top border to white to create a spinner effect */
  width: 50px; /* Adjust the width and height of the spinner */
  height: 50px;
  animation: spin 1s linear infinite; /* Add a spinning animation */
}

@keyframes spin {
  0% { transform: rotate(0deg); } /* Start rotating from 0 degrees */
  100% { transform: rotate(360deg); } /* End rotating at 360 degrees */
}

</style>
