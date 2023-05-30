<template>
  <q-page padding>
    <div>
      <RenderTable
        :columns="suppliesColumns"
        :rows="supplies"
        title="Insumos"
        detail_query="/supplies/"
        row_key="id"
        addTo="/supplies/new_supply"
      />
    </div>
    <div class="q-mt-xl">
      <RenderTable
        :columns="lotsColumns"
        :rows="lots"
        title="Lotes"
        detail_query="/supplies/lot/"
        row_key="id"
        addTo="/supplies/new_lot"
      />
    </div>
  </q-page>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import {suppliesColumns, lotsColumns} from '../constants/columns.js'

const lots = ref([]);
const supplies = ref([]);
const api_prefix = process.env.API;

const getLots = () => {
  axios
    .get(api_prefix + "/lots")
    .then((response) => (lots.value = response.data));
};

const getSupplies = () => {
  axios
    .get(api_prefix + "/supplies")
    .then((response) => (supplies.value = response.data));
};

onMounted(() => {
  getLots();
  getSupplies();
});
</script>
