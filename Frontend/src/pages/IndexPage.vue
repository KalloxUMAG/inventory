<template>
  <q-page class="flex flex-center content-start">
    <div class="critic-tables q-mt-md">

      <RenderTable
          :columns="suppliesColumns"
          :rows="supplies"
          title="Insumos criticos"
          detail_query="/supplies/"
          row_key="id"
        />
    </div>
  </q-page>
</template>

<script setup>
import { defineComponent, onMounted, ref } from 'vue'
import {suppliesColumns} from '../constants/columns.js'
import axios from "axios";
import RenderTable from 'src/components/RenderTable.vue';

const api_prefix = process.env.API_URL;

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

<style>
.critic-tables{
  width: 90%;
}
</style>