<template>
  <div fluid>
    <v-row>
      <v-col xl="5" lg="6" md="6" sm="6" cols="12" class="pos pr-0">
        <ItemsSelector></ItemsSelector>
      </v-col>
      <v-col xl="7" lg="6" md="6" sm="6" cols="12" class="pos">
        <ItemsCrads></ItemsCrads>
      </v-col>
    </v-row>
  </div>
</template>


<script>
import ItemsSelector from "./ItemsSelector.vue";
import ItemsCrads from "./ItemsCrads.vue";

export default {
  data: function () {
    return {};
  },
  components: {
    ItemsSelector,
    ItemsCrads,
  },
  methods: {},
};
</script>

<style scoped>
</style>