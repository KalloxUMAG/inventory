<template>
  <PageTitle title="Inicio" icon="home" />
  <StatisticsSection
    :equipments="equipmentsQuantity"
    :supplies="suppliesQuantity"
    :critical-equipments="criticalEquipmentsQuantity"
    :critical-supplies="criticalSuppliesQuantity"
  />
  <div class="row">
    <div class="col">
      <q-card class="no-shadow bg-transparent">
        <q-card-section class="q-pl-none col-12">
          <div class="text-subtitle1 q-pl-md">
            Insumos con bajo stock
            <q-btn flat icon-right="arrow_forward" label="Ver todos" to="/supplies/" class="text-gray-8 non-selectable no-outline float-right" />
          </div>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <CriticTable
            :columns="suppliesColumns"
            :rows="criticalSupplies"
            detail_query="/supplies/"
            row_key="id"
          />
        </q-card-section>
      </q-card>

      <q-card class="no-shadow bg-transparent">
        <q-card-section class="q-pl-none col-12">
          <div class="text-subtitle1 q-pl-md">
            Equipos con mantenimiento proximo
            <q-btn flat icon-right="arrow_forward" label="Ver todos" to="/equipments/" class="text-gray-8 non-selectable no-outline float-right" />
          </div>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <CriticTable
            :columns="equipmentsColumns"
            :rows="criticalEquipments"
            detail_query="/equipments/"
            row_key="id"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import CriticTable from 'src/components/CriticTable/CriticTable.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'
import StatisticsSection from 'src/components/statistics/StatisticsSection.vue'
import { getCriticalEquipments, getCriticalSupplies, getEquipments, getSupplies } from 'src/services/index.js'
import { equipmentsColumns, suppliesColumns } from '../constants/columns.js'

const criticalEquipments = ref([])
const criticalEquipmentsQuantity = ref(0)
const criticalSupplies = ref([])
const criticalSuppliesQuantity = ref(0)
const equipmentsQuantity = ref(0)
const suppliesQuantity = ref(0)

async function getEquipmentsData() {
  criticalEquipments.value = await getCriticalEquipments()
  criticalEquipmentsQuantity.value = criticalEquipments.value.length
  const equipments = await getEquipments()
  equipmentsQuantity.value = equipments.length
}

async function getSuppliesData() {
  criticalSupplies.value = await getCriticalSupplies()
  criticalSuppliesQuantity.value = criticalSupplies.value.length
  const supplies = await getSupplies()
  suppliesQuantity.value = supplies.length
}

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
  getEquipmentsData()
  getSuppliesData()
})
</script>
