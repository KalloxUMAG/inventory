<template>
  <div class="row q-col-gutter-sm">
    <div class="col-md-3 col-sm-12 col-xs-12">
      <StatisticCounter color="#23978a" icon="biotech" title="Equipos" :value="equipments" />
    </div>
    <div class="col-md-3 col-sm-12 col-xs-12">
      <StatisticCounter color="#48b06d" icon="science" title="Insumos" :value="supplies" />
    </div>
    <div class="col-md-3 col-sm-12 col-xs-12">
      <StatisticCounter color="#644d99" icon="settings" title="Mantenimientos próximos" :value="criticalEquipments" />
    </div>
    <div class="col-md-3 col-sm-12 col-xs-12">
      <StatisticCounter color="#104e95" icon="call" title="Insumos críticos" :value="criticalSupplies" />
    </div>
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

</script>\
