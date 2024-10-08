<template>
  <PageTitle title="Insumos" icon="science" />
  <q-card class="no-shadow card-style" bordered>
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md row">
        <div class="text-weight-bold col-12 col-lg-4">
          Lista de insumos
        </div>
        <div class="col-12 col-lg-8">
          <div class="actions-buttons float-right">
            <q-input
              v-model="filter"
              outlined
              bg-color="white"
              dense
              debounce="300"
              placeholder="Buscar"
            >
              <template #append>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-btn
              class="add-btn"
              to="/supplies/new_supply"
              icon="add"
              label="Agregar"
              flat
            />
          </div>
        </div>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section class="q-pa-xs">
      <q-table
        :grid="$q.screen.xs"
        row-key="id"
        :columns="suppliesColumns"
        :rows="supplies"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        flat
        bordered
        no-wrap
        :filter="filter"
        class="card-style"
        @row-click="rowClicker"
      >
        <template #header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              class="text-italic table-header" :class="[col.additionalClass]"
            >
              {{ col.label }}
            </q-th>
            <q-th auto-width>
              Lotes
            </q-th>
          </q-tr>
        </template>
        <template #body="props">
          <q-tr :props="props" class="item-row">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              @click="rowClicker(props.row)"
            >
              <div v-if="col.name === 'state'" class="state-col">
                <q-icon v-if="props.row.state" name="error" color="red">
                  <q-tooltip class="bg-negative" :offset="[10, 10]">
                    Bajo stock
                  </q-tooltip>
                </q-icon>
              </div>
              <div v-else>
                {{ col.value }}
              </div>
            </q-td>
            <q-td auto-width>
              <q-btn size="sm" align="between" color="accent" flat :icon-right="props.expand ? 'expand_less' : 'expand_more'" @click="props.expand = !props.expand" />
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td class="subtable" colspan="100%">
              <q-table
                :grid="$q.screen.xs"
                :rows="props.row.lots"
                :columns="lotsColumns"
                row-key="id"
                flat
                no-wrap
                hide-bottom
                card-class="bg-grey-1 text-grey-8"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

import PageTitle from 'src/components/commons/PageTitle.vue'
import { lotsColumns, suppliesColumns } from '../constants/columns.js'

const supplies = ref([])
const api_prefix = process.env.API_URL

const router = useRouter()
const filter = ref('')
const detail_query = '/supplies/'
const $q = useQuasar()

async function getSupplies() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies`,
    })
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock
      supply.critical = supply.stock <= supply.critical_stock
      return supply
    })
  }
  catch (error) {}
}

function rowClicker(row) {
  const item = row.id
  router.push(detail_query + item)
}

onMounted(() => {
  getSupplies()
})
</script>

<style scoped>
 .card-style{
  border-radius: 12px;
 }
 .space-between{
  display: flex;
  justify-content: space-between;
 }
 .actions-buttons{
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
 }
 .item-row{
  cursor: pointer;
 }
 .subtable{
  padding: 0;
 }
</style>
