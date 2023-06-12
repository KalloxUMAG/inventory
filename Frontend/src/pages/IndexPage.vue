<template>
  <q-page class="flex flex-center">
    <RenderTable
        :columns="suppliesColumns"
        :rows="supplies"
        title="Insumos criticos"
        detail_query="/supplies/"
        row_key="id"
      />
  </q-page>
</template>

<script setup>
import { defineComponent, onMounted, ref } from 'vue'
import {suppliesColumns} from '../constants/columns.js'
import axios from "axios";
import RenderTable from 'src/components/RenderTable.vue';

const api_prefix = process.env.API;

const supplies = ref([])

const getSupplies = () => {
  axios
    .get(api_prefix + "/supplies/critical")
    .then((response) => (supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      return supply;
    })))
};

onMounted(() => {
  getSupplies();
});

</script>
