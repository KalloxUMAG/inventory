<template>
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
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import { sendRequest } from "src/axios/instance";
import { suppliesColumns, lotsColumns } from "../constants/columns.js";

const lots = ref([]);
const supplies = ref([]);
const api_prefix = process.env.API_URL;

const getSupplies = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies",
    });
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      supply.critical = supply.stock <= supply.critical_stock ? true : false;
      return supply;
    });
  } catch (error) {}
};

onMounted(() => {
  getSupplies();
});
</script>
