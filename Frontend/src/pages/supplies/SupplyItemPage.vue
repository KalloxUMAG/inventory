<template>
  <div v-if="supply != null" class="col justify-center">
    <PageTitle :title="supply.name" icon="science">
      <div>
        <q-btn
          outline
          color="secondary"
          label="Editar"
          @click="editSupply"
        />
        <!--
        <q-btn
          class="q-ml-sm"
          color="negative"
          label="Eliminar"
          @click="removeSupply"
        />
        -->
      </div>
    </PageTitle>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-6">
        <q-card class="bg-white no-shadow card_style" flat bordered>
          <q-card-section>
            <InfoSection
              title="Datos Insumo" :fields="[
                {
                  label: 'Nombre',
                  value: supply.name,
                },
                {
                  label: 'Código',
                  value: supply.code,
                },
                {
                  label: 'Marca',
                  value: supply.supplies_brand_name,
                },
                {
                  label: 'Tipo',
                  value: supply.supplies_type_name,
                },
                {
                  label: 'Formato',
                  value: supply.supplies_format_name,
                },
                {
                  label: 'Stock actual',
                  value: `${supply.stock} unidades`,
                },
                {
                  label: 'Stock por lote',
                  value: `${supply.lot_stock} unidades por lote`,
                },
                {
                  label: 'Stock crítico',
                  value: supply.critical_stock,
                },
                {
                  label: 'Muestras por unidad',
                  value: supply.samples,
                },
                {
                  label: 'Muestras totales',
                  value: supply.samples * supply.stock,
                },
                {
                  label: 'Temperatura de consevación',
                  value: supply.temperature,
                },
                {
                  label: 'Observación',
                  value: supply.observation,
                },
              ]"
            />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-6">
        <q-card class="bg-white full-height card_style" flat bordered>
          <q-card-section>
            <div class="text-h5 text-weight-bold q-pl-md space-between">
              Proveedores
              <div class="actions-buttons">
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
                  class="add-btn q-mr-sm"
                  icon="add"
                  label="Agregar"
                  flat
                  @click="addSupplier"
                />
              </div>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-xs">
            <q-table
              :grid="$q.screen.xs"
              row-key="id"
              :columns="suppliersSupplyColumns"
              :rows="suppliers"
              no-data-label="No hay registros para mostrar"
              rows-per-page-label="Registros por pagina"
              flat
              bordered
              no-wrap
              :filter="filter"
              class="card-style"
            >
              <template #header="props">
                <q-tr :props="props">
                  <q-th
                    v-for="col in props.cols"
                    :key="col.name"
                    :props="props"
                    class="text-italic table-header"
                  >
                    {{ col.label }}
                  </q-th>
                </q-tr>
              </template>
              <template #body-cell="props">
                <q-td
                  :props="props"
                >
                  {{ props.value }}
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
    <div class="q-mt-md col-12">
      <q-card class="no-shadow q-pa-xs card_style" flat bordered>
        <q-card-section class="q-pl-none">
          <div class="text-h5 text-weight-bold q-pl-md space-between">
            Lotes
            <div class="actions-buttons">
              <q-input
                v-model="lotsFilter"
                outlined
                dense
                debounce="300"
                placeholder="Buscar"
              >
                <template #append>
                  <q-icon name="search" />
                </template>
              </q-input>
              <q-btn
                class="add-btn q-mr-sm"
                icon="add"
                label="Agregar"
                flat
                @click="addLot"
              />
            </div>
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-pa-xs">
          <q-table
            :grid="$q.screen.xs"
            row-key="id"
            :columns="lotsColumns"
            :rows="lots"
            no-data-label="No hay registros para mostrar"
            rows-per-page-label="Registros por pagina"
            flat
            bordered
            no-wrap
            :filter="lotsFilter"
            class="card-style"
          >
            <template #header="props">
              <q-tr :props="props">
                <q-th
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                  class="text-italic table-header"
                >
                  {{ col.label }}
                </q-th>
              </q-tr>
            </template>
            <template #body-cell="props">
              <q-td
                :props="props"
              >
                {{ props.value }}
              </q-td>
            </template>
            <template #body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  dense
                  icon="edit"
                  color="warning"
                  @click="editLot(props.row)"
                />
                <q-btn
                  v-if="props.row.id != null"
                  flat
                  dense
                  icon="delete"
                  color="negative"
                  @click="removeLot(props.row)"
                />
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>
    <div v-if="groupStocks.length > 0" class="q-mt-md">
      <StockChart :key="chartKey" title="Stocks por grupo" :data="groupStocks" :critical="supply.critical_stock" />
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import { useQuasar } from 'quasar'
import { sendRequest } from 'src/services/axios/instance.js'
import PageTitle from 'src/components/commons/PageTitle.vue'
import { lotsColumns, suppliersSupplyColumns } from 'src/constants/columns.js'
import { deleteLot, getGroupsStock } from 'src/services/index'

import InfoSection from 'src/components/item-page/InfoSection.vue'
import StockChart from 'src/components/statistics/StockChart.vue'
import AddSupplier from '../AddSupplier.vue'
import AddLot from '../AddLot.vue'
import EditLot from '../EditLot.vue'
import EditSupply from '../EditSupply.vue'

const route = useRoute()
const id = computed(() => route.params.id)
const supply = ref(null)
const suppliers = ref([])
const lots = ref([])
const groupStocks = ref([])

const filter = ref('')
const lotsFilter = ref('')

const $q = useQuasar()
const router = useRouter()

const api_prefix = process.env.API_URL

const chartKey = ref(0)

watch(groupStocks, () => {
  chartKey.value += 1
})

async function getSupply() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies/${id.value}`,
    })
    supply.value = response.data
  }
  catch (error) {}
}

async function getSuppliers() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers_supplies/${id.value}`,
    })
    suppliers.value = response.data
  }
  catch (error) {}
}

async function loadGroupStock() {
  groupStocks.value = await getGroupsStock(id.value)
}

async function getLots() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/lots/supply/${id.value}`,
    })
    lots.value = response.data
  }
  catch (error) {}
}

function addSupplier() {
  $q.dialog({
    component: AddSupplier,
    componentProps: {
      supply_id: supply.value.id,
    },
  }).onOk((data) => {
    getSuppliers()
  })
}

function addLot() {
  $q.dialog({
    component: AddLot,
    componentProps: {
      supply_id: supply.value.id,
      stock: supply.value.lot_stock,
    },
  }).onOk(async(data) => {
    await getLots()
    await getSupply()
    await loadGroupStock()
  })
}

function removeLot(lot) {
  $q.dialog({
    title: 'Eliminar lote',
    message: 'Se eliminara el lote y se descontara del stock actual del insumo',
    ok: {
      color: 'negative',
      label: 'Aceptar y eliminar',
    },
    cancel: {
      color: 'warning',
      label: 'Cancelar y mantener',
    },
  })
    .onOk(async () => {
      const lot_id = lot.id
      await deleteLot(lot_id)
      await getLots()
      await getSupply()
      await loadGroupStock()
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    })
}

function editLot(lot) {
  $q.dialog({
    component: EditLot,
    componentProps: {
      supply_id: supply.value.id,
      lot_id: lot.id,
      number: lot.number,
      supplier: { id: lot.supplier_id, name: lot.supplier_name },
      observation: lot.observations,
      reception_date: lot.reception_date,
      due_date: lot.due_date,
      stock: lot.stock,
      location: { id: lot.location_id, name: lot.location },
      sublocation: { id: lot.sub_location_id, name: lot.sub_location },
      project: { id: lot.project_id, name: lot.project },
      group: lot.group_id,
      group_default: { id: lot.group_id, name: lot.group_name },
    },
  })
    .onOk(async(data) => {
      await getLots()
      await getSupply()
      await loadGroupStock()
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    })
}

function editSupply() {
  $q.dialog({
    component: EditSupply,
    componentProps: {
      supply_id: supply.value.id,
      brand: {
        id: supply.value.supplies_brand_id,
        name: supply.value.supplies_brand_name,
      },
      type: {
        id: supply.value.supplies_type_id,
        name: supply.value.supplies_type_name,
      },
      name: supply.value.name,
      code: supply.value.code,
      format: {
        id: supply.value.supplies_format_id,
        name: supply.value.supplies_format_name,
      },
      samples: supply.value.samples,
      stock: supply.value.stock,
      lot_stock: supply.value.lot_stock,
      temperature: { id: supply.value.temperature, name: supply.value.temperature },
      observation: supply.value.observation,
      critical_stock: supply.value.critical_stock,
    },
  })
    .onOk((data) => {
      getSupply()
    })
    .onCancel(() => {})
}

function removeSupply() {
  $q.dialog({
    title: 'Eliminar insumo',
    message:
      'El insumo sera archivado y solo podra ser recuperado por un administrador',
    ok: {
      color: 'negative',
      label: 'Aceptar y eliminar',
    },
    cancel: {
      color: 'warning',
      label: 'Cancelar y mantener',
    },
  })
    .onOk(async () => {
      try {
        const response = await sendRequest({
          method: 'DELETE',
          url: `${api_prefix}/supplies/${id.value}`,
        })
        redirectToSupplies()
      }
      catch (error) {}
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    })
}

function redirectToSupplies() {
  router.push({ path: '../supplies' })
}

onMounted(() => {
  getSupply()
  getSuppliers()
  getLots()
  loadGroupStock()
})
</script>

<style scoped>
.container {
  border: 1px solid #d1d1d1 !important;
  border-radius: 12px !important;
  padding: 8px;
  overflow: visible;
}

.card_style {
  border-radius: 12px;
}

.border-none {
  border: none !important;
}

.gap-lg{
  gap: 24px;
}

.full-height {
  min-height: 100%;
}

.image-visor{
  border: none !important;
  height: 250px;
  widows: 250px;
  padding: 0;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}

.no-image{
    align-items: center;
    background-color: #eef3f7;
    color: #6c757d;
    display: flex;
    height: 100%;
    justify-content: center;
    font-size: 24px;
}

.actions-buttons{
  display: inline-flex;
  gap: 10px;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
}

.space-between{
  display: flex;
  justify-content: space-between;
}

.maintenance-table {
  width: 100%;
}
</style>
