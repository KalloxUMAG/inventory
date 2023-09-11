<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form @submit="onOKClick" ref="EditLotForm">
        <div class="text-bold text-subtitle1 q-my-sm">Datos lote</div>
        <!--Fields-->
        <div class="col">
          <div class="row q-my-sm">
            <SelectForm
              outlined
              class="col"
              :options="suppliersOptions"
              option_value="id"
              option_label="name"
              label="Proveedor"
              :default_value="props.supplier"
              not_found_label="No hay proveedores disponibles"
              @updateModel="
                (value) => {
                  supplier = value;
                }
              "
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              outlined
              v-model="number"
              label="Número de lote"
              class="col q-mr-sm"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              outlined
              class="col"
              v-model="due_date"
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
              outlined=""
              class="col"
              type="text"
              stack-label
              label="Observación"
              v-model="observation"
            />
          </div>
          <div class="row">
            <div v-if="!newLocationState" class="col q-mt-md">
              <SelectForm
                outlined
                class="row q-mr-md"
                :disable="disableLocation"
                :options="locationOptions"
                option_value="id"
                option_label="name"
                :default_value="props.location"
                label="Localización"
                not_found_label="No hay localizaciones disponibles"
                @updateModel="
                  (value) => {
                    location = value;
                    getSublocations();
                  }
                "
                :rules="[(val) => !!val || 'Campo obligatorio']"
                lazy-rules
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
                  outlined
                  v-model="newLocation"
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
              <SelectForm
                outlined
                class="row"
                :disable="disableSublocation"
                :options="sublocationOptions"
                option_value="id"
                option_label="name"
                :default_value="props.sublocation"
                label="Sub-localización"
                not_found_label="No hay sublocalizaciones disponibles"
                @updateModel="
                  (value) => {
                    sublocation = value;
                  }
                "
                :rules="[(val) => !!val || 'Campo obligatorio']"
                lazy-rules
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
                  outlined
                  v-model="newSublocation"
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
              @click="disableLocation = false"
              class="q-mr-sm"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              @click="
                newSublocation != ''
                  ? newLocationState == true
                    ? newLocation != ''
                      ? (disableLocation = true)
                      : ''
                    : location != null
                    ? (disableLocation = true)
                    : ''
                  : ''
              "
              class="q-mr-sm"
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
          <SelectForm
            outlined
            class="row"
            :options="projectOptions"
            option_value="id"
            option_label="name"
            :default_value="props.project"
            label="Proyectos"
            not_found_label="No hay proyectos disponibles"
            @updateModel="
              (value) => {
                project = value;
              }
            "
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
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
              outlined
              v-model="newProject"
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
            @click="newProject != '' ? (disableProject = !disableProject) : ''"
            class="q-mr-sm"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="(newProjectState = false), (disableProject = false)"
          />
        </div>
        <div v-if="newProjectState" class="row">
          <div v-if="!newProjectOwnerState" class="col">
            <SelectForm
              outlined
              class="row"
              :disable="disableProjectOwner"
              :options="projectOwnersOptions"
              option_value="id"
              option_label="name"
              label="Dueño proyecto"
              not_found_label="No hay dueños disponibles"
              @updateModel="
                (value) => {
                  projectOwner = value;
                }
              "
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
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
              outlined
              class="row"
              v-model="newProjectOwner"
              label="Nombre dueño"
              :disable="disableProjectOwner"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
            <div class="row justify-end q-mt-md">
              <q-btn
                :label="disableProjectOwner ? 'Editar' : 'Guardar'"
                color="amber"
                @click="
                  newProjectOwner != ''
                    ? (disableProjectOwner = !disableProjectOwner)
                    : ''
                "
                class="q-mr-sm"
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
        <!--Buttons-->
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
import axios from "axios";
import { useDialogPluginComponent, useQuasar } from "quasar";
import { onMounted, ref, toRefs } from "vue";
import { sendRequest } from "src/axios/instance";
import SelectForm from "src/components/SelectForm.vue";
const api_prefix = process.env.API_URL;

const props = defineProps({
  supply_id: Number,
  lot_id: Number,
  number: String,
  supplier: Object,
  observation: String,
  due_date: String,
  location: Object,
  sublocation: Object,
  project: Object,
});

const number = ref(props.number);
const supplier = ref(props.supplier.id);
const observation = ref(props.observation);
const due_date = ref(props.due_date);
const location = ref(props.location.id);
const sublocation = ref(props.sublocation.id);
const project = ref(props.project.id);
const projectOwner = ref(null);

const newLocationState = ref(false);
const disableLocation = ref(false);
const newSublocationState = ref(false);
const disableSublocation = ref(false);
const disableProject = ref(false);
const disableProjectOwner = ref(false);
const newProjectState = ref(false);
const newProjectOwnerState = ref(false);
const newLocation = ref("");
const newSublocation = ref("");
const newProject = ref("");
const newProjectOwner = ref("");

const suppliersOptions = ref([]);
const locationOptions = ref([]);
const sublocationOptions = ref([]);
const projectOptions = ref([]);
const projectOwnersOptions = ref([]);

const EditLotForm = ref(null);

const $q = useQuasar();

const getSuppliers = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/suppliers_supplies/" + props.supply_id,
    });
    suppliersOptions.value = response.data;
  } catch (error) {}
};

const getProjects = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/projects",
    });
    projectOptions.value = response.data;
  } catch (error) {}
};

const getProjectOwners = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/project_owners",
    });
    const projectsowners = response.data;
    projectOwnersOptions.value = projectsowners.map((x) => {
      return { id: x.id, name: x.name };
    });
  } catch (error) {}
};

const getLocations = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/locations",
    });
    locationOptions.value = response.data;
  } catch (error) {}
};

const getSublocations = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/sub_locations/" + location.value,
    });
    sublocationOptions.value = response.data;
  } catch (error) {}
};

async function createNewLocation() {
  if (!newLocationState.value) {
    return location.value;
  }
  const data = {
    name: newLocation.value,
  };
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/locations",
      data: data,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la localizacion: " + error,
    });
  }
}

async function createNewSublocation(location_id) {
  if (!newLocationState.value && !newSublocationState.value) {
    return sublocation.value;
  }
  const data = {
    name: newSublocation.value,
    location_id: location_id,
  };
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/sub_locations",
      data: data,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la sublocalizacion: " + error,
    });
  }
}

async function editLot(data) {
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/lots/" + props.lot_id,
      data: data,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo editar el lote: " + error,
    });
    return -1;
  }
}

async function createNewProject(project_owner_id) {
  if (!newProjectState.value) {
    return project.value;
  }

  const projectName = newProject.value;

  if (projectName.trim().length == 0) {
    return -1;
  }

  if (project_owner_id == -1) {
    project_owner_id = null;
  }

  const projectData = {
    name: projectName,
    owner_id: project_owner_id,
  };

  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/projects",
      data: projectData,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el proyecto: " + error,
    });
  }
}

async function createNewProjectOwner() {
  if (!newProjectOwnerState.value) {
    return projectOwner.value;
  }

  const projectOwnerName = newProjectOwner.value;

  if (projectOwnerName.trim().length == 0) {
    return -1;
  }

  const projectOwnerData = {
    name: projectOwnerName,
  };

  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/project_owners",
      data: projectOwnerData,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el dueño: " + error,
    });
  }
}

onMounted(() => {
  getSuppliers();
  getProjects();
  getProjectOwners();
  getLocations();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

async function onOKClick() {
  EditLotForm.value.resetValidation();

  const data = {
    number: number.value,
    due_date: due_date.value,
    observations: observation.value,
    sub_location_id: sublocation.value,
    state: true,
    supply_id: props.supply_id,
    project_id: project.value,
    supplier_id: supplier.value,
  };

  const project_owner_id = await createNewProjectOwner();
  const project_id = await createNewProject(project_owner_id);
  data["project_id"] = project_id;
  const location_id = await createNewLocation();
  const sub_location_id = await createNewSublocation(location_id);

  data["sub_location_id"] = sub_location_id;

  await editLot(data);

  onDialogOK();
}
</script>
