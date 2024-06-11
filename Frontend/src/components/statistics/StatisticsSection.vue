<template>
  <div class="statistics-container">
    <StatisticCounter color="#23978a" icon="biotech" title="Equipos" :value="equipments" />
    <StatisticCounter color="#48b06d" icon="science" title="Insumos" :value="supplies" />
    <StatisticCounter color="#644d99" icon="settings" title="Mantenimientos próximos" :value="criticalEquipments" />
    <StatisticCounter color="#104e95" icon="call" title="Insumos críticos" :value="criticalSupplies" />
  </div>
</template>

<script setup>
import { toRefs } from 'vue'
import StatisticCounter from 'src/components/statistics/StatisticsCounter.vue'

const props = defineProps({
  equipments: {
    type: Number,
    default: 0,
  },
  supplies: {
    type: Number,
    default: 0,
  },
  criticalEquipments: {
    type: Number,
    default: 0,
  },
  criticalSupplies: {
    type: Number,
    default: 0,
  },
})

const { equipments, supplies, criticalEquipments, criticalSupplies } = toRefs(props)

</script>

<style scoped>
  .statistics-container {
    display: flex;
    gap: 20px;
    margin-top: 20px;
  }
</style>
