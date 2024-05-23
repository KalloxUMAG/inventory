<template>
  <div class="statistics-container">
    <StatisticCounter color="#23978a" icon="biotech" title="Equipos" value="1" />
    <StatisticCounter color="#48b06d" icon="science" title="Insumos" value="0" />
    <StatisticCounter color="#644d99" icon="settings" title="Mantenimientos próximos" value="1" />
    <StatisticCounter color="#104e95" icon="call" title="Insumos críticos" value="0" />
  </div>
</template>

<script setup>
import StatisticCounter from 'src/components/statistics/StatisticsCounter.vue'
import { getEquipmentList } from '/src/services'

const equipments = getEquipmentList()
</script>

<style scoped>
  .statistics-container {
    display: flex;
    gap: 20px;
    margin-top: 20px;
  }
</style>
