<template>
  <q-page padding>
    <RenderTable :columns="equipmentsColumns" :rows="equipments" title="Equipamiento" detail_query="/equipments/" row_key="id" addTo="/equipments/new_equipment"/>
  </q-page>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import axios from 'axios'
import { onMounted, ref } from "vue";
import {equipmentsColumns} from '../constants/columns.js'

const equipments = ref([])

const api_prefix = process.env.API;

const getEquipments = () => {
  axios.get(api_prefix+"/equipments").then(
        response => (
          equipments.value = response.data
        )
      )
}

onMounted( () => {
  getEquipments();
})

</script>
