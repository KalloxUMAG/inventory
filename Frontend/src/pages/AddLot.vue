<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form ref="AddLotForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1 q-my-sm">
          Datos lote
        </div>
        <!-- Fields -->
        <div class="col">
          <div class="row q-my-sm">
            <InputSelect
              outlined
              class="col"
              :options="suppliersOptions"
              option_value="id"
              option_label="name"
              label="Proveedor"
              not_found_label="No hay proveedores disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  supplier = value;
                }
              "
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              v-model="number"
              outlined
              label="Número de lote"
              class="col q-mr-sm"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              v-model="lot_stock"
              outlined
              label="Stock inicial"
              class="col q-mr-sm"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              v-model="reception_date"
              outlined
              class="col"
              type="date"
              label="Fecha de recepcion*"
              stack-label
              lazy-rules
              :rules="[
                (val) => (val && val != null) || 'Este campo es obligatorio',
              ]"
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              v-model="due_date"
              outlined
              class="col"
              type="date"
              label="Fecha de vencimiento*"
              stack-label
              lazy-rules
              :rules="[
                (val) => (val && val != null) || 'Este campo es obligatorio',
              ]"
            />
          </div>
          <div class="row">
            <q-input
              v-model="observation"
              outlined=""
              class="col"
              type="text"
              stack-label
              label="Observación"
            />
          </div>
          <div class="row">
            <div v-if="!newLocationState" class="col q-mt-md">
              <InputSelect
                outlined
                class="row q-mr-md"
                :disable="disableLocation"
                :options="locationOptions"
                option_value="id"
                option_label="name"
                label="Localización"
                not_found_label="No hay localizaciones disponibles"
                :rules="[(val) => !!val || 'Campo obligatorio']"
                lazy-rules
                @update-model="
                  (value) => {
                    location = value;
                    getSublocations();
                  }
                "
              />
              <div class="row justify-end q-pt-md">
                <q-btn
                  label="Añadir localización"
                  icon="add"
                  class="add-btn text-caption q-mr-md"
                  @click="newLocationState = !newLocationState"
                />
              </div>
            </div>
            <div v-else class="col q-mt-md">
              <div class="row">
                <q-input
                  v-model="newLocation"
                  outlined
                  label="Nombre localización"
                  class="col"
                  :disable="disableLocation"
                  :rules="[(val) => !!val || 'Campo obligatorio']"
                  lazy-rules
                />
              </div>
            </div>
            <div
              v-if="!newLocationState && !newSublocationState"
              class="col q-mt-md"
            >
              <InputSelect
                outlined
                class="row"
                :disable="disableSublocation"
                :options="sublocationOptions"
                option_value="id"
                option_label="name"
                label="Sub-localización"
                not_found_label="No hay sublocalizaciones disponibles"
                :rules="[(val) => !!val || 'Campo obligatorio']"
                lazy-rules
                @update-model="
                  (value) => {
                    sublocation = value;
                  }
                "
              />
              <div class="row justify-end q-pt-md">
                <q-btn
                  outlined
                  label="Añadir sub-localización"
                  icon="add"
                  class="add-btn text-caption"
                  @click="newSublocationState = !newSublocationState"
                />
              </div>
            </div>
            <div v-else class="col q-mt-md">
              <div class="row">
                <q-input
                  v-model="newSublocation"
                  outlined
                  label="Nombre sub-localización"
                  class="col"
                  :disable="disableLocation"
                  :rules="[(val) => !!val || 'Campo obligatorio']"
                  lazy-rules
                />
              </div>
            </div>
          </div>
        </div>
        <div class="col q-mt-sm">
          <div
            v-if="newLocationState || newSublocationState"
            class="row justify-end"
          >
            <q-btn
              v-if="disableLocation"
              label="Editar"
              color="amber"
              class="q-mr-sm"
              @click="disableLocation = false"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              class="q-mr-sm"
              @click="
                newSublocation !== ''
                  ? newLocationState === true
                    ? newLocation !== ''
                      ? (disableLocation = true)
                      : ''
                    : location != null
                      ? (disableLocation = true)
                      : ''
                  : ''
              "
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (newLocationState = false),
                (newSublocationState = false),
                (disableLocation = false)
              "
            />
          </div>
        </div>
        <div v-if="!newProjectState" class="col">
          <InputSelect
            outlined
            class="row"
            :options="projectOptions"
            option_value="id"
            option_label="name"
            label="Proyectos"
            not_found_label="No hay proyectos disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                project = value;
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Proyecto"
              icon="add"
              class="add-btn text-caption"
              @click="newProjectState = !newProjectState"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="newProject"
              outlined
              label="Nombre proyeto"
              class="col"
              :disable="disableProject"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="newProjectState" class="row justify-end">
          <q-btn
            :label="disableProject ? 'Editar' : 'Guardar'"
            color="amber"
            class="q-mr-sm"
            @click="newProject !== '' ? (disableProject = !disableProject) : ''"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="(newProjectState = false), (disableProject = false)"
          />
        </div>
        <div v-if="newProjectState" class="row">
          <div v-if="!newProjectOwnerState" class="col">
            <InputSelect
              outlined
              class="row"
              :disable="disableProjectOwner"
              :options="projectOwnersOptions"
              option_value="id"
              option_label="name"
              label="Dueño proyecto"
              not_found_label="No hay dueños disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  projectOwner = value;
                }
              "
            />
            <div class="row justify-end q-mt-md">
              <q-btn
                label="Añadir dueño"
                color="amber"
                class="add-btn"
                @click="newProjectOwnerState = true"
              />
            </div>
          </div>
          <div v-else class="col">
            <q-input
              v-model="newProjectOwner"
              outlined
              class="row"
              label="Nombre dueño"
              :disable="disableProjectOwner"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
            <div class="row justify-end q-mt-md">
              <q-btn
                :label="disableProjectOwner ? 'Editar' : 'Guardar'"
                color="amber"
                class="q-mr-sm"
                @click="
                  newProjectOwner !== ''
                    ? (disableProjectOwner = !disableProjectOwner)
                    : ''
                "
              />
              <q-btn
                label="Ver lista"
                color="amber"
                @click="
                  (disableProjectOwner = false), (newProjectOwnerState = false)
                "
              />
            </div>
          </div>
        </div>
        <div class="row">
          <div v-if="defaultGroup" class="col">
            <InputSelect
              outlined
              class="row"
              :clearable="false"
              :options="groupsOptions"
              :default_value="defaultGroup"
              option_value="group_id"
              option_label="group_name"
              label="Grupo"
              not_found_label="No hay grupos disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  group = value;
                }
              "
            />
          </div>
        </div>
        <!-- Buttons -->
        <div class="q-mt-md row justify-end">
          <q-btn
            color="primary"
            label="Guardar"
            type="submit"
            class="q-mr-sm"
          />
          <q-btn color="negative" label="Cancelar" @click="onDialogCancel" />
        </div>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent, useQuasar } from 'quasar'
import { onMounted, ref } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'
import { getMyGroups, postLot } from 'src/services/index.js'

import InputSelect from 'src/components/form/inputs/InputSelect.vue'

const props = defineProps({
  supply_id: Number,
  stock: Number,
})

defineEmits([...useDialogPluginComponent.emits])

const api_prefix = process.env.API_URL

const number = ref(0)
const lot_stock = ref(0)
const supplier = ref(null)
const observation = ref('')
const reception_date = ref(null)
const due_date = ref(null)
const location = ref(null)
const sublocation = ref(null)
const project = ref(null)
const projectOwner = ref(null)
const group = ref(null)
const defaultGroup = ref(null)

const newLocationState = ref(false)
const disableLocation = ref(false)
const newSublocationState = ref(false)
const disableSublocation = ref(false)
const disableProject = ref(false)
const disableProjectOwner = ref(false)
const newProjectState = ref(false)
const newProjectOwnerState = ref(false)
const newLocation = ref('')
const newSublocation = ref('')
const newProject = ref('')
const newProjectOwner = ref('')

const groupsOptions = ref([])
const suppliersOptions = ref([])
const locationOptions = ref([])
const sublocationOptions = ref([])
const projectOptions = ref([])
const projectOwnersOptions = ref([])

const AddLotForm = ref(null)

const $q = useQuasar()

async function getSuppliers() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers_supplies/${props.supply_id}`,
    })
    suppliersOptions.value = response.data
  }
  catch (error) {}
}

async function getGroupsData() {
  groupsOptions.value = await getMyGroups()
  if (groupsOptions.value.length > 0) {
    defaultGroup.value = { group_id: groupsOptions.value[0].group_id, group_name: groupsOptions.value[0].group_name }
    group.value = defaultGroup.value.group_id
  }
  else {
    defaultGroup.value = { group_id: null, group_name: null }
  }
}

async function getProjects() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/projects`,
    })
    projectOptions.value = response.data
  }
  catch (error) {}
}

async function getProjectOwners() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/project_owners`,
    })
    const projectowners = response.data
    projectOwnersOptions.value = projectowners.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getLocations() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/locations`,
    })
    locationOptions.value = response.data
  }
  catch (error) {}
}

async function getSublocations() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/sub_locations/${location.value}`,
    })
    sublocationOptions.value = response.data
  }
  catch (error) {}
}

async function createNewLocation() {
  if (!newLocationState.value)
    return location.value

  const data = {
    name: newLocation.value,
  }
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/locations`,
      data,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la localizacion: ${error}`,
    })
  }
}

async function createNewSublocation(location_id) {
  if (!newLocationState.value && !newSublocationState.value)
    return sublocation.value

  const data = {
    name: newSublocation.value,
    location_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/sub_locations`,
      data,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la sublocalizacion: ${error}`,
    })
  }
}

async function createNewProject(project_owner_id) {
  if (!newProjectState.value)
    return project.value

  const projectName = newProject.value

  if (projectName.trim().length === 0)
    return -1

  if (project_owner_id === -1)
    project_owner_id = null

  const projectData = {
    name: projectName,
    owner_id: project_owner_id,
  }
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/projects`,
      data: projectData,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el proyecto: ${error}`,
    })
  }
}

async function createNewProjectOwner() {
  if (!newProjectOwnerState.value)
    return projectOwner.value

  const projectOwnerName = newProjectOwner.value

  if (projectOwnerName.trim().length === 0)
    return -1

  const projectOwnerData = {
    name: projectOwnerName,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/project_owners`,
      data: projectOwnerData,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el dueño: ${error}`,
    })
  }
}

onMounted(() => {
  getGroupsData()
  getSuppliers()
  getProjects()
  getProjectOwners()
  getLocations()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
  = useDialogPluginComponent()

async function onOKClick() {
  AddLotForm.value.resetValidation()

  const data = {
    number: number.value,
    lot_stock: lot_stock.value,
    reception_date: reception_date.value,
    due_date: due_date.value,
    observations: observation.value,
    supply_id: props.supply_id,
    sub_location_id: sublocation.value,
    project_id: project.value,
    supplier_id: supplier.value.supplier_id,
    group_id: group.value,
  }

  const project_owner_id = await createNewProjectOwner()
  const project_id = await createNewProject(project_owner_id)
  data.project_id = project_id
  const location_id = await createNewLocation()
  const sub_location_id = await createNewSublocation(location_id)

  data.sub_location_id = sub_location_id

  await postLot(data)

  onDialogOK()
}
</script>
