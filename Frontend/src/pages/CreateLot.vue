<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent="onSubmit"
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
        ref="createLotForm"
      >
        <!--Datos Producto-->
        <h5>Agregar lotes</h5>
        <div class="section-title">
          Datos Insumo
          <hr />
        </div>
        <!--Select supply-->
        <SelectForm
          outlined
          :options="suppliesOptions"
          option_value="id"
          option_label="name"
          label="Insumos"
          not_found_label="No hay insumos disponibles"
          @updateModel="(value) => (supply = value)"
          class="col q-ml-md"
        />

        <q-input
          outlined
          v-model="code"
          maxlength="49"
          label="Código lote*"
          lazy-rules
          :rules="[
            (val) => (val && val.length > 0) || 'Este campo es obligatorio',
            (val) =>
              (val && val.length < 50) ||
              'El nombre debe contener menos de 50 caracteres',
          ]"
        />

        <div class="row justify-center">
          <q-input
            outlined
            class="col"
            type="number"
            v-model="stock"
            maxlength="49"
            label="Stock"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Este campo es obligatorio',
              (val) => (val && val > 0) || 'El stock debe ser mayor que 0',
            ]"
          />

          <q-input
            outlined
            class="col q-ml-md"
            type="number"
            v-model="criticalStock"
            maxlength="49"
            label="Stock critico"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Este campo es obligatorio',
              (val) =>
                (val && val > 0) || 'El stock critico debe ser mayor que 0',
            ]"
          />
        </div>

        <q-input
          outlined
          v-model="dueDate"
          type="date"
          label="Fecha de vencimiento*"
          stack-label
          lazy-rules
          :rules="[
            (val) => (val && val != null) || 'Este campo es obligatorio',
          ]"
        />

        <q-input
          outlined
          class="col q-ml-md"
          type="number"
          v-model="samples"
          maxlength="49"
          label="Muestras"
          lazy-rules
        />

        <q-input
          outlined
          v-model="observation"
          type="textarea"
          label="Observación"
          lazy-rules
        />

        <!--Project-->

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

        <!--Location-->
        <div class="row justify-center">
          <div v-if="!newLocationState" class="col q-mr-md">
            <SelectForm
              outlined
              class="row q-mr-md"
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
          <div v-else class="col">
            <div class="row">
              <q-input
                outlined
                v-model="newLocation"
                label="Localización"
                class="col"
                :disable="disableLocation"
              />
            </div>
          </div>
          <div v-if="!newLocationState && !newSublocationState" class="col">
            <SelectForm
              outlined
              class="row"
              :options="sublocationOptions"
              option_value="id"
              option_label="name"
              label="Sub-localización"
              not_found_label="No hay una sub-localizaciones disponibles"
              @updateModel="
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
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input
                outlined
                v-model="newSublocation"
                label="Sub-localización"
                class="col"
                :disable="disableSublocation"
              />
            </div>
          </div>
        </div>

        <div
          v-if="newLocationState || newSublocationState"
          class="row justify-end"
        >
          <q-btn
            :label="disableLocation ? 'Editar' : 'Guardar'"
            color="amber"
            @click="
              (disableLocation = !disableLocation),
                (disableSublocation = !disableSublocation)
            "
            class="q-mr-sm"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="(newLocationState = false), (newSublocationState = false)"
          />
        </div>

        <!--Form button-->
        <div class="row justify-end q-mt-mx">
          <q-btn label="Crear" type="submit" color="positive" />
        </div>
        <q-inner-loading
          :showing="loading"
          label="Creando lote"
          label-class="text-deep-orange"
          label-style="font-size: 1.6em"
        />
      </q-form>
    </div>
  </q-page>
</template>

<script setup>
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";
import SelectForm from "src/components/SelectForm.vue";

//Options Selects
const suppliesOptions = ref([]);
const locationOptions = ref([]);
const projectOptions = ref([]);
const projectOwnersOptions = ref([]);
const sublocationOptions = ref([]);

//Models
const code = ref(null);
const criticalStock = ref(null);
const dueDate = ref(null);
const observation = ref(null);
const project = ref(null);
const projectOwner = ref(null);
const samples = ref(null);
const stock = ref(null);
const supply = ref(null);
const location = ref(null);
const sublocation = ref(null);
const newLocation = ref(null);
const newProject = ref(null);
const newProjectOwner = ref(null);
const newSublocation = ref(null);

//Flags
const newLocationState = ref(false);
const newProjectState = ref(false);
const newProjectOwnerState = ref(false);
const newSublocationState = ref(false);
const disableLocation = ref(false);
const disableProject = ref(false);
const disableProjectOwner = ref(false);
const disableSublocation = ref(false);
const loading = ref(false);

//Form
const createLotForm = ref(null);
const $q = useQuasar();

//Get functions

const getSupplies = () => {
  axios.get("http://localhost:8000/api/supplies").then((response) => {
    const supplies = response.data;
    suppliesOptions.value = supplies.map((x) => {
      const name = `${x.name} | ${x.supplies_brand_name} | ${x.code} | ${x.supplier_name}`;
      return { id: x.id, name: name };
    });
  });
};

const getLocations = () => {
  axios.get("http://localhost:8000/api/locations").then((response) => {
    const locations = response.data;
    locationOptions.value = locations.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getProjects = () => {
  axios.get("http://localhost:8000/api/projects").then((response) => {
    const projects = response.data;
    projectOptions.value = projects.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getProjectOwners = () => {
  axios.get("http://localhost:8000/api/project_owners").then((response) => {
    const projectsowners = response.data;
    projectOwnersOptions.value = projectsowners.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSublocations = () => {
  if (location.value == null) {
    sublocation.value = null;
    sublocationOptions.value = [];
  } else {
    axios
      .get("http://localhost:8000/api/sub_locations/" + location.value)
      .then((response) => {
        const sublocations = response.data;
        sublocationOptions.value = sublocations.map((x) => {
          return { id: x.id, name: x.name };
        });
      });
  }
};

//Create functions

async function createNewLocation(){
  if(!newLocationState.value){
    return location.value;
  }

  if (location.value.trim().length == 0) {
    return -1;
  }

  const locationData = {
    'name': location.value
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/api/locations",
      locationData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la ubicación: " + error,
    });
  }
}

async function createNewLot(lotData){
  try {
    const response = await axios.post(
      "http://localhost:8000/api/lots",
      lotData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el lote: " + error,
    });
  }
}

async function createNewSublocation(location_id){
  if(!newSublocationState.value && !newLocationState.value){
    return sublocation.value;
  }

  if (sublocation.value.trim().length == 0) {
    return -1;
  }

  const sublocationData = {
    name: sublocation.value,
    location_id: location_id
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/api/sub_locations",
      sublocationData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la sub-ubicación: " + error,
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
    const response = await axios.post(
      "http://localhost:8000/api/projects",
      projectData
    );
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
      "http://localhost:8000/api/project_owners",
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

async function onSubmit() {
  createLotForm.value.resetValidation();
  let lot = {
    number: code.value,
    due_date: dueDate.value,
    full_stock: criticalStock.value,
    stock: stock.value,
    samples: samples.value,
    observations: observation.value,
    supplies_id: supply.value,
    sub_location_id: sublocation.value,
    project_id: project.value,
  };

  loading.value = true;

  const project_owner_id = await createNewProjectOwner();
  const project_id = await createNewProject(project_owner_id);

  lot['project_id'] = project_id;

  const location_id = await createNewLocation();
  const sub_location_id = await createNewSublocation(location_id);
  if(sub_location_id == -1){
    loading.value = false;
    return;
  }
  const lot_id = await createNewLot(lot);

  loading.value = false;
}

onMounted(() => {
  getSupplies();
  getLocations();
  getProjects();
  getProjectOwners();
  getSublocations();
});
</script>

<style scoped>
body {
  background-image: url(./../assets/background.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

hr {
  width: 20%;
  height: 2px;
  background-color: black;
}

.section-title {
  text-align: center;
  font-weight: bold;
  font-size: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

.add-btn {
  background-color: #7b7bd2 !important;
  color: #fff;
  border: 2px solid #7777cf;
}

.q-form {
  margin-top: 10px;
  background-color: #fffffe;
  border-radius: 1%;
  border-width: 1px;
  border-style: solid;
}
</style>
