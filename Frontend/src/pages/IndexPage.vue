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
    <div class="critic-tables q-mt-md">
      <RenderTable
        :columns="criticEquipmentsColumns"
        :rows="equipments"
        title="Equipos criticos"
        detail_query="/equipments/"
        row_key="id"
      />
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { suppliesColumns, criticEquipmentsColumns, equipmentsColumns } from "../constants/columns.js";
import { sendRequest } from "src/axios/instance.js";
import RenderTable from "src/components/RenderTable.vue";
import { useQuasar } from "quasar";

const api_prefix = process.env.API_URL;

const equipments = ref([]);
const supplies = ref([]);
const $q = useQuasar();

const getSupplies = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies/critical",
    });
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      return supply;
    });
  } catch (error) {
    if (error.respose.status === 403) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "Sesion expirada, favor inciar sesion de nuevo",
      });
    }
  }
};

const getEquipments = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/equipments/nextmaintenances",
    });
    equipments.value = response.data
  } catch (error) {
    if (error.respose.status === 403) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "Sesion expirada, favor inciar sesion de nuevo",
      });
    }
  }
};

onMounted(() => {
  getEquipments();
  getSupplies();
});
</script>

<style>
.critic-tables {
  width: 90%;
}
</style>
