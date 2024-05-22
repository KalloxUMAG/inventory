<template>
  <div class="row q-col-gutter-md">
    <div class="flex col">
      <q-card class="my-card fit" flat bordered>
        <q-item class="row justify-center">
          <div class="text-h5 text-weight-bold">
            Datos insumo
            <q-btn
              class="q-ml-md glossy"
              icon="edit"
              color="positive"
              @click="editSupply"
            />
          </div>
        </q-item>
        <q-separator />
        <!-- Datos producto -->
        <q-card-section>
          <div class="col q-pa-sm">
            <div class="row q-mb-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Nombre
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.name }}
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Código
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.code }}
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Marca
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.supplies_brand_name }}
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Tipo
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.supplies_type_name }}
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Formato
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.supplies_format_name }}
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Stock actual
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.stock }} unidades
              </div>
            </div>
            <q-separator />
            <div class="row q-my-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Stock por lote
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.lot_stock }} unidades por lote.
              </div>
            </div>
            <q-separator />
            <div class="row q-mt-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Stock crítico
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.critical_stock }}
              </div>
            </div>
            <q-separator />
            <div class="row q-mt-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Muestras por unidad
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.samples }}
              </div>
            </div>
            <q-separator />
            <div class="row q-mt-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Muestras totales
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.samples * supply.stock }}
              </div>
            </div>
            <q-separator />
            <div class="row q-mt-sm">
              <div class="col-5 text-h6 text-weight-bold q-pl-md">
                Observación
              </div>
              <div class="col text-h6 text-grey-8">
                {{ supply.observation }}
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div class="flex col">
      <q-card class="my-card fit" flat bordered>
        <q-card-section horizontal>
          <q-separator vertical />
          <!-- Datos producto -->
          <div class="col">
            <NoRedirectTable
              title="Proveedores"
              :columns="suppliersSupplyColumns"
              :rows="suppliers"
              :add-function="addSupplier"
            />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
  <div class="row q-mt-md">
    <div class="col">
      <NoRedirectTable
        title="Lotes"
        :columns="lotsColumns"
        :rows="lots"
        :add-function="addLot"
        :edit-function="editLot"
        :delete-function="removeLot"
      />
    </div>
  </div>
  <div class="row q-mt-md justify-end">
    <q-btn
      label="Eliminar"
      color="negative"
      class="text-h6"
      @click="removeSupply"
    />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import NoRedirectTable from 'src/components/NoRedirectTable.vue'
import { useQuasar } from 'quasar'
import { sendRequest } from 'src/axios/instance'
import { lotsColumns, suppliersSupplyColumns } from '../constants/columns.js'
import AddSupplier from './AddSupplier.vue'
import AddLot from './AddLot.vue'
import EditLot from './EditLot.vue'
import EditSupply from './EditSupply.vue'

const route = useRoute()
const id = computed(() => route.params.id)
const supply = ref({})
const suppliers = ref([])
const lots = ref([])

const $q = useQuasar()
const router = useRouter()

const api_prefix = process.env.API_URL

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
  }).onOk((data) => {
    getLots()
    getSupply()
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
      const lot_stock = supply.value.lot_stock * -1
      try {
        const response = await sendRequest({
          method: 'PUT',
          url: `${api_prefix}/lots/deactivate${lot_id}`,
        })
        getLots()
      }
      catch (error) {}

      const data = {
        stock: lot_stock,
      }
      try {
        const response = await sendRequest({
          method: 'PUT',
          url: `${api_prefix}/supplies/stock/${id.value}`,
          data,
        })
        getSupply()
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
      location: { id: lot.location_id, name: lot.location },
      sublocation: { id: lot.sub_location_id, name: lot.sub_location },
      project: { id: lot.project_id, name: lot.project },
    },
  })
    .onOk((data) => {
      getLots()
      getSupply()
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
})
</script>

<style scoped>
.field-label {
  font-size: 16px;
  font-weight: bold;
}

.field-content {
  font-size: 16px;
  font-weight: 500;
}

.col {
  height: 100%;
}
</style>
