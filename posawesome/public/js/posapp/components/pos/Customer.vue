<template>
  <v-row class="items px-2 py-1">
    <v-col cols="12" class="pb-0 mb-2">
      <v-autocomplete
        dense
        clearable
        autofocus
        auto-select-first
        outlined
        color="indigo"
        label="Customer"
        v-model="cutomer"
        :items="cutomers"
        append-outer-icon="mdi-plus"
        background-color="white"
        no-data-text="Customer not found"
        hide-details
      ></v-autocomplete>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    cutomers: ["Cash Customer", "foo", "bar", "fizz", "buzz"],
    cutomer: "Cash Customer",
  }),
};
</script>