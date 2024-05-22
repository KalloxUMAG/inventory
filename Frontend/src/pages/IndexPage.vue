<template>
  <PageTitle title="Inicio" icon="home" />
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
            :rows="supplies"
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
            :rows="equipments"
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
import { sendRequest } from 'src/axios/instance.js'
import CriticTable from 'src/components/CriticTable/CriticTable.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'
import { useQuasar } from 'quasar'
import { equipmentsColumns, suppliesColumns } from '../constants/columns.js'

const api_prefix = process.env.API_URL

const equipments = ref([])
const supplies = ref([])
const $q = useQuasar()

async function getSupplies() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies/critical`,
    })
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock
      return supply
    })
  }
  catch (error) {
    if (error.respose.status === 403) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: 'Sesion expirada, favor inciar sesion de nuevo',
      })
    }
  }
}

async function getEquipments() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/equipments/nextmaintenances`,
    })
    equipments.value = response.data
  }
  catch (error) {
    if (error.respose.status === 403) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: 'Sesion expirada, favor inciar sesion de nuevo',
      })
    }
  }
}

onMounted(() => {
  getEquipments()
  getSupplies()
})
</script>
