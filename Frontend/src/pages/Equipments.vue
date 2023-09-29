<template>
  <q-page padding>
    <RenderTable
      :columns="equipmentsColumns"
      :rows="equipments"
      title="Equipamiento"
      detail_query="/equipments/"
      row_key="id"
      addTo="/equipments/new_equipment"
    />
  </q-page>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import { onMounted, ref } from "vue";
import { equipmentsColumns } from "../constants/columns.js";

import { useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance";

const router = useRouter();

const equipments = ref([]);

const api_prefix = process.env.API_URL;

const getEquipments = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/equipments",
    });
    equipments.value = response.data;
  } catch (error) {
  }
};

onMounted(() => {
  getEquipments();
});
</script>
