<template>
  <PageTitle title="Inicio" icon="home" />
  <StatisticsSection
    :equipments="equipmentsQuantity"
    :supplies="suppliesQuantity"
    :critical-equipments="criticalEquipmentsQuantity"
    :critical-supplies="criticalSuppliesQuantity"
  />
  <div class="row">
    <div class="col-12">
      <CriticTable
        title="Insumos con stock bajo"
        :columns="suppliesColumns"
        :rows="criticalSupplies"
        detail_query="/supplies/"
        row_key="id"
      />
    </div>
    <div class="col-12">
      <CriticTable
      title="Equipos con mantenimiento proximo"
        :columns="equipmentsColumns"
        :rows="criticalEquipments"
        detail_query="/equipments/"
        row_key="id"
      />
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

onMounted(() => {
  getEquipmentsData()
  getSuppliesData()
})
</script>
