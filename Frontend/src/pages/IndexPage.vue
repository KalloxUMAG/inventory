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
import { onMounted, ref } from "vue";
import { suppliesColumns } from "../constants/columns.js";
import { reqInstance, sendRequest } from "src/axios/instance.js";
import RenderTable from "src/components/RenderTable.vue";

import { useRouter } from "vue-router";

const api_prefix = process.env.API_URL;

const supplies = ref([]);
const router = useRouter();

const getSupplies = async () => {
  try {
    const response = await reqInstance.get(api_prefix + "/supplies/critical");
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      return supply;
    });
  } catch (error) {
    if (error.response.status === 403) {
      router.push({ path: "/login" });
    }
  }
};
/*
const getSupplies = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies/critical",
    });
    console.log(response);
    supplies.value = response.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      return supply;
    });
  } catch (error) {
    console.log(error);
  }
};*/

onMounted(() => {
  getSupplies();
});
</script>

<style>
.critic-tables {
  width: 90%;
}
</style>
