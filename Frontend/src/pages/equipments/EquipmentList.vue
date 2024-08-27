<template>
  <PageTitle title="Equipos" icon="biotech" />
  <q-card class="no-shadow card-style" bordered>
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md row">
        <div class="text-weight-bold col-12 col-lg-4">
          Lista de equipamientos
        </div>
        <div class="col-12 col-lg-8">
          <div class="actions-buttons float-right">
            <SelectForm
              outlined
              dense
              bg-color="white"
              :options="projects"
              option_value="id"
              option_label="name"
              label="Filtrar por Proyecto"
              not_found_label="No hay modelos disponibles"
              @update-model="
                (value) => {
                  equipmentFilters.project = value
                  filterEquipment()
                }
              "
            />
            <SelectForm
              outlined
              dense
              bg-color="white"
              :options="equipmentTypes"
              option_value="id"
              option_label="name"
              label="Filtrar por Tipo de equipo"
              not_found_label="No hay tipos de equipo disponibles"
              @update-model="
                (value) => {
                  equipmentFilters.equipmentType = value
                  filterEquipment()
                }
              "
            />
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
              to="/equipments/new_equipment"
              icon="add"
              label="Agregar"
              flat
            />
          </div>
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-pa-xs">
      <q-table
        :grid="$q.screen.xs"
        row-key="id"
        :columns="equipmentsColumns"
        :rows="filteredEquipments"
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
          <q-td :props="props" auto-width>
            <!-- Mostrar icono si state es false, de lo contrario mostrar texto normal -->
            <div class="state-col">
              <q-icon v-if="!props.row.state" name="error" color="red">
                <q-tooltip class="bg-negative" :offset="[10, 10]">
                  Realizar mantenimiento
                </q-tooltip>
              </q-icon>
            </div>
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

import PageTitle from 'src/components/commons/PageTitle.vue'
import SelectForm from 'src/components/SelectForm.vue'
import { getEquipmentTypes, getEquipments, getProjects } from 'src/services/index.js'
import { equipmentsColumns } from '../../constants/columns.js'

const router = useRouter()
const $q = useQuasar()

const equipments = ref([])
const equipmentTypes = ref([])
const filteredEquipments = ref([])
const projects = ref([])
const equipmentFilters = reactive({
  project: null,
  equipmentType: null,
})
const filter = ref('')

const detail_query = '/equipments/'

async function getEquipmentsData() {
  equipments.value = await getEquipments()
  filteredEquipments.value = equipments.value
}

async function getProjectsData() {
  projects.value = await getProjects()
}

async function getEquipmentTypesData() {
  equipmentTypes.value = await getEquipmentTypes()
}

function filterEquipment() {
  filteredEquipments.value = equipments.value
  if (equipmentFilters.project) {
    filteredEquipments.value = filteredEquipments.value.filter(equipment => equipment.project_id === equipmentFilters.project)
  }
  if (equipmentFilters.equipmentType) {
    filteredEquipments.value = filteredEquipments.value.filter(equipment => equipment.equipment_type_id === equipmentFilters.equipmentType)
  }
}

function rowClicker(e, row) {
  const item = row.id
  router.push(detail_query + item)
}

onMounted(() => {
  getEquipmentsData()
  getEquipmentTypesData()
  getProjectsData()
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
  gap: 10px;
  justify-content: flex-end;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
 }
</style>
