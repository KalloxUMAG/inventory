<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form @submit="onOKClick" ref="AddLotForm">
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
              not_found_label="No hay proveedores disponibles"
              @updateModel="
                (value) => {
                  supplier = value;
                }
              "
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              outlined
              v-model="number"
              label="Número"
              class="col q-mr-sm"
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
            <q-input
              outlined
              type="number"
              v-model="stock"
              label="Stock"
              class="col q-ml-sm"
              :rules="[val => !!val || 'Campo obligatorio']"
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
                label="Localización"
                not_found_label="No hay localizaciones disponibles"
                @updateModel="
                  (value) => {
                    location = value;
                    getSublocations();
                  }
                "
                :rules="[val => !!val || 'Campo obligatorio']"
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
                  :rules="[val => !!val || 'Campo obligatorio']"
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
                label="Sub-localización"
                not_found_label="No hay sublocalizaciones disponibles"
                @updateModel="
                  (value) => {
                    sublocation = value;
                  }
                "
                :rules="[val => !!val || 'Campo obligatorio']"
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
                  :rules="[val => !!val || 'Campo obligatorio']"
                  lazy-rules
                />
              </div>
            </div>
          </div>
        </div>
        <div class="col q-mt-sm">
          <div v-if="newLocationState || newSublocationState" class="row justify-end">
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
              @click="disableLocation = true"
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
            label="Proyectos"
            not_found_label="No hay proyectos disponibles"
            @updateModel="
              (value) => {
                project = value;
              }
            "
            :rules="[val => !!val || 'Campo obligatorio']"
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
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="newProjectState" class="row justify-end">
          <q-btn
            :label="disableProject ? 'Editar' : 'Guardar'"
            color="amber"
            @click="disableProject = !disableProject"
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
              :rules="[val => !!val || 'Campo obligatorio']"
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
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
            <div class="row justify-end q-mt-md">
              <q-btn
                :label="disableProjectOwner ? 'Editar' : 'Guardar'"
                color="amber"
                @click="disableProjectOwner = !disableProjectOwner"
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
import SelectForm from "src/components/SelectForm.vue";
const api_prefix = process.env.API_URL;

const number = ref(0);
const stock = ref(0);
const supplier = ref(null);
const observation = ref('');
const due_date = ref(null);
const location = ref(null);
const sublocation = ref(null);
const project = ref(null);
const projectOwner = ref(null);

const newLocationState = ref(false);
const disableLocation = ref(false);
const newSublocationState = ref(false);
const disableSublocation = ref(false);
const disableProject = ref(false)
const disableProjectOwner = ref(false)
const newProjectState = ref(false);
const newProjectOwnerState = ref(false);
const newLocation = ref(null);
const newSublocation = ref(null);
const newProject = ref(null)
const newProjectOwner = ref(null);


const suppliersOptions = ref([]);
const locationOptions = ref([]);
const sublocationOptions = ref([]);
const projectOptions = ref([]);
const projectOwnersOptions = ref([])

const AddLotForm = ref(null);

const $q = useQuasar();

const props = defineProps({
  supply_id: Number,
});

const getSuppliers = () => {
  axios
    .get(api_prefix + "/suppliers_supplies/" + props.supply_id)
    .then((response) => (suppliersOptions.value = response.data));
};

const getProjects = () => {
  axios
    .get(api_prefix + "/projects")
    .then((response) => (projectOptions.value = response.data));
};

const getProjectOwners = () => {
  axios.get(api_prefix + "/project_owners").then((response) => {
    const projectsowners = response.data;
    projectOwnersOptions.value = projectsowners.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getLocations = () => {
  axios
    .get(api_prefix + "/locations")
    .then((response) => (locationOptions.value = response.data));
};

const getSublocations = () => {
  axios
    .get(api_prefix + "/sub_locations/" + location.value)
    .then((response) => (sublocationOptions.value = response.data));
};

async function createNewLocation() {
  if (!newLocationState.value) {
    return location.value;
  }
  const data = {
    name: newLocation.value,
  };
  try {
    const response = await axios.post(api_prefix + "/locations", data);
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
    location_id: location_id
  };
  try {
    const response = await axios.post(api_prefix + "/sub_locations", data);
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

async function createNewLot(data){
  try {
    const response = await axios.post(api_prefix + "/lots", data);
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el insumo: " + error,
    });
    return -1
  }
}

async function updateStock(supply_id, stock){
  //Update stock on database
  const data = {
    stock: stock
  }
  try {
    const response = await axios.put(api_prefix + "/supplies/" + supply_id, data);
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo modificar el stock del insumo: " + error,
    });
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
    const response = await axios.post(api_prefix + "/projects", projectData);
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
    const response = await axios.post(
      api_prefix + "/project_owners",
      projectOwnerData
    );
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
  AddLotForm.value.resetValidation();

  const data = {
    number: number.value,
    due_date: due_date.value,
    stock: stock.value,
    observations: observation.value,
    supply_id: props.supply_id,
    sub_location_id: sublocation.value,
    project_id: project.value,
    supplier_id: supplier.value.supplier_id,
  };

  const project_owner_id = await createNewProjectOwner();
  const project_id = await createNewProject(project_owner_id);
  data["project_id"] = project_id
  const location_id = await createNewLocation();
  const sub_location_id = await createNewSublocation(location_id);

  data['sub_location_id'] = sub_location_id;

  const lot_id = await createNewLot(data);

  if (lot_id != -1){
    await updateStock(props.supply_id, stock.value)
  }
  onDialogOK();
}
</script>
