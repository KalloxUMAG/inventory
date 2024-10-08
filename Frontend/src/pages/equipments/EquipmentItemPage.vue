<template>
  <div v-if="equipment != null" class="col justify-center">
    <PageTitle :title="equipment.name" icon="biotech">
      <div>
        <q-btn
          outline
          color="secondary"
          label="Editar"
          @click="editEquipment"
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
        <q-card class="bg-white full-height card_style" flat bordered>
          <q-card-section>
            <Carousel v-if="img_api" :api_endpoint="img_api" />
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-6">
        <q-card class="bg-white no-shadow card_style" flat bordered>
          <q-card-section>
            <InfoSection
              title="Información general" :fields="[
                {
                  label: 'Nombre',
                  value: equipment.name,
                },
                {
                  label: 'Codigo serial',
                  value: equipment.serial_number,
                },
                {
                  label: 'Inventario UMAG',
                  value: equipment.umag_inventory_code,
                },
                {
                  label: 'Marca',
                  value: equipment.brand_name,
                },
                {
                  label: 'Modelo',
                  value: equipment.model_name,
                },
                {
                  label: 'Número de modelo',
                  value: equipment.model_number,
                },
                {
                  label: 'Tipo de equipo',
                  value: equipment.equipment_type_name ?? 'Sin información',
                },
                {
                  label: 'Periodo de mantención',
                  value: maintenance_period,
                },
                {
                  label: 'Observación',
                  value: equipment.observation,
                },
                {
                  label: '¿Es relevante?',
                  value: equipment.relevant ? 'Si' : 'No',
                }
              ]"
            />
            <InfoSection
              title="Ubicación" :fields="[
                {
                  label: 'Edificio',
                  value: equipment.building_name,
                },
                {
                  label: 'Unidad',
                  value: equipment.unit_name,
                },
                {
                  label: 'Sala',
                  value: equipment.room_name,
                },
              ]"
            />
            <InfoSection
              title="Compra" :fields="[
                {
                  label: 'Proveedor',
                  value: equipment.supplier_name,
                },
                {
                  label: 'Fecha de recepción',
                  value: equipment.reception_date,
                },
                {
                  label: 'Factura',
                  value: equipment.invoice_number,
                },
                {
                  label: 'Proyecto',
                  value: equipment.project_name ? equipment.project_name : 'Sin información',
                },
                {
                  label: 'Etapa',
                  value: equipment.stage_name ? equipment.stage_name : 'Sin información',
                },
              ]"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>
    <div
      v-if="equipment.maintenance_period !== null"
      class="q-mt-md maintenance-table"
    >
      <div class="q-mt-md col">
        <q-card class="no-shadow q-pa-xs card_style" flat bordered>
          <q-card-section class="q-pl-none">
            <div class="text-h5 text-weight-bold q-pl-md space-between">
              Lista de Mantenimientos
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
                  @click="addFunction"
                />
              </div>
            </div>
          </q-card-section>
          <q-card-section class="q-pa-none">
            <q-table
              :grid="$q.screen.xs"
              row-key="id"
              :columns="columns_maintenances"
              :rows="maintenances"
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
              <template #body-cell-state="props">
                <q-td
                  :props="props"
                >
                  <q-icon
                    v-if="props.row.state === true"
                    size="md"
                    name="done_all"
                    color="positive"
                  >
                    <q-tooltip>Realizado</q-tooltip>
                  </q-icon>
                  <q-icon
                    v-if="props.row.state === false"
                    size="md"
                    name="close"
                    color="negative"
                  >
                    <q-tooltip>No realizado</q-tooltip>
                  </q-icon>
                  <q-icon
                    v-if="props.row.state == null"
                    size="md"
                    name="play_arrow"
                    color="warning"
                  >
                    <q-tooltip>Próximo</q-tooltip>
                  </q-icon>
                </q-td>
              </template>
              <template #body-cell-actions="props">
                <q-td :props="props">
                  <q-btn
                    flat
                    dense
                    icon="edit"
                    color="warning"
                    @click="editMaintenance(props.row)"
                  />
                  <q-btn
                    v-if="props.row.id != null"
                    flat
                    dense
                    icon="delete"
                    color="negative"
                    @click="removeMaintenance(props.row)"
                  />
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import Carousel from 'src/components/Carousel.vue'
import FormModal from 'src/components/FormModal.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'
import { useQuasar } from 'quasar'
import { columns_maintenances } from 'src/constants/columns.js'
import { deleteMaintenance, getEquipment, getLastMaintenance, getMaintenances, postMaintenance } from 'src/services'

import InfoSection from 'src/components/item-page/InfoSection.vue'
import EditMaintenance from '../EditMaintenance.vue'

const $q = useQuasar()
const router = useRouter()

const content_loaded = ref(false)
const filter = ref('')
const img_api = ref(null)
const equipment = ref(null)
const maintenances = ref([])
const last_maintenance = ref({})
const maintenance_period = ref(null)

const api_prefix = process.env.API_URL

const route = useRoute()
const id = computed(() => route.params.id)

function padTo2Digits(num) {
  return num.toString().padStart(2, '0')
}

function formatDate(date) {
  return [
    date.getFullYear(),
    padTo2Digits(date.getMonth() + 1),
    padTo2Digits(date.getDate()),
  ].join('-')
}

function createNextMaintenance() {
  const dateString = last_maintenance.value ? `${last_maintenance.value.date}T00:00:00` : `${equipment.value.reception_date}T00:00:00`
  const months = equipment.value.maintenance_period
  let date = new Date(dateString)
  date.setDate(date.getDate() + months * 30)
  date = formatDate(date)
  const data = {
    id: null,
    date,
    observations: 'Próxima mantención programada',
    state: null,
    maintenance_type: 'Programada',
    equiptment_id: equipment.value.id,
  }
  maintenances.value.unshift(data)
  maintenances.value.sort((x, y) => {
    const date1 = new Date(`${x.date}T00:00:00`)
    const date2 = new Date(`${y.date}T00:00:00`)
    if (date1 < date2)
      return -1

    return 1
  })
}

async function getEquipmentData() {
  equipment.value = await getEquipment(id.value)
  img_api.value = `${api_prefix}/equipments/image/${equipment.value.id}`
  maintenance_period.value = equipment.value.maintenance_period ? `Cada ${equipment.value.maintenance_period} meses` : 'No aplica'
  maintenances.value = await getMaintenances(id.value)
  last_maintenance.value = await getLastMaintenance(id.value)
  createNextMaintenance()
}

function addFunction() {
  $q.dialog({
    component: FormModal,
    componentProps: {
      title: 'Agregar mantenimiento',
      fields: [
        {
          label: 'Fecha',
          type: 'date',
          defaultvalue: null,
          rules: [val => (val && val != null) || 'Este campo es obligatorio'],
        },
        {
          label: 'Tipo de mantenimiento',
          type: 'select',
          defaultvalue: null,
          options: [
            { id: 'Programada', name: 'Programada' },
            { id: 'Correctiva', name: 'Correctiva' },
          ],
          option_value: 'id',
          option_label: 'name',
          not_found_label: 'No hay tipos de mantenimiento',
          rules: [val => (val && val != null) || 'Este campo es obligatorio'],
        },
        {
          label: 'Estado',
          type: 'select',
          defaultvalue: null,
          options: [
            { id: '0', name: 'Sin realizar' },
            { id: '1', name: 'Realizado' },
          ],
          option_value: 'id',
          option_label: 'name',
          not_found_label: ' ',
          rules: [val => (val && val != null) || 'Este campo es obligatorio'],
        },
        {
          label: 'Observaciones',
          type: 'text',
          defaultvalue: null,
          autogrow: true,
          rules: [val => (val && val != null) || 'Este campo es obligatorio'],
        },
      ],
    },
  })
    .onOk(async (data) => {
      const state = data[2] === 1 ? true : data[2] === 0 ? false : null
      const maintenance_data = {
        date: data[0],
        observations: data[3],
        maintenance_type: data[1],
        state,
        equiptment_id: equipment.value.id,
      }

      await postMaintenance(maintenance_data)
      maintenances.value = await getMaintenances(id.value)
      last_maintenance.value = await getLastMaintenance(id.value)
      createNextMaintenance()
    })
    .onCancel(() => {})
}

function editMaintenance(maintenance) {
  $q.dialog({
    component: EditMaintenance,
    componentProps: {
      id: maintenance.id,
      date_value: maintenance.date,
      type_value: {
        id: maintenance.maintenance_type,
        name: maintenance.maintenance_type,
      },
      typeOptions: [
        { id: 'Programada', name: 'Programada' },
        { id: 'Correctiva', name: 'Correctiva' },
      ],
      state_value: {
        id: maintenance.state ? 1 : 0,
        name: maintenance.state ? 'Realizado' : 'Sin realizar',
      },
      stateOptions: [
        { id: '0', name: 'Sin realizar' },
        { id: '1', name: 'Realizado' },
      ],
      observation_value: maintenance.observations,
      equiptment_id: maintenance.equiptment_id,
    },
  }).onOk(async () => {
    maintenances.value = await getMaintenances(id.value)
    last_maintenance.value = await getLastMaintenance(id.value)
    createNextMaintenance()
  })
}

function editEquipment() {
  router.push(`/equipments/edit/${id.value}`)
}

function removeMaintenance(maintenance) {
  $q.dialog({
    title: 'Eliminar mantenimiento',
    message: 'Se eliminara el mantenimiento',
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
      const maintenance_id = maintenance.id
      await deleteMaintenance(maintenance_id)
      maintenances.value = await getMaintenances(id.value)
      last_maintenance.value = await getLastMaintenance(id.value)
      createNextMaintenance()
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    })
}

onMounted(() => {
  getEquipmentData()
  content_loaded.value = true
})
</script>

<style scoped>
.item-title{
  align-content: center;
}

.card_style {
  border-radius: 12px;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}

.container{
  border: 1px solid #d1d1d1 !important;
  border-radius: 12px !important;
  padding: 8px;
  overflow: visible;
}

.gap-lg{
  gap: 24px;
}

.image-visor{
  border: none !important;
  max-height: 500px;
  padding: 0;
}

.maintenance-table {
  width: 100%;
}
.field-label {
  font-size: 16px;
  font-weight: bold;
}

.field-content {
  font-size: 16px;
  font-weight: 500;
}

.card-style{
  border-radius: 12px;
}
.space-between{
  display: flex;
  justify-content: space-between;
}
.actions-buttons{
  display: inline-flex;
  gap: 10px;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
}
</style>
