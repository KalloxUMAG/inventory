<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent="onSubmit"
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
        ref="createSupplyForm"
      >
        <!--Datos Producto-->
        <h5>Agregar insumos</h5>
        <div class="section-title">
          Datos Insumo
          <hr />
        </div>
        <div class="col">
          <div class="row">
            <q-input
              outlined
              v-model="supply.name"
              label="Nombre*"
              class="col q-mr-md"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
            <q-input
              outlined
              v-model="supply.code"
              label="Codigo*"
              class="col"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div class="col">
          <div class="row">
            <q-input
              outlined
              v-model="supply.samples"
              label="Muestras por unidad*"
              type="number"
              step="any"
              class="col q-mr-md"
              :rules="[(val) => (val.length > 0 && val != null) || 'Campo obligatorio']"
            />
            <q-input
              outlined
              v-model="supply.lot_stock"
              label="Stock por lote*"
              type="number"
              step="any"
              class="col"
              :rules="[(val) => (val.length > 0 && val != null) || 'Campo obligatorio']"
            />
          </div>
        </div>
        <div class="col">
          <div class="row">
            <q-input
              outlined
              v-model="supply.critical_stock"
              label="Stock crítico*"
              type="number"
              class="col"
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="!flags.newBrandState" class="col">
          <SelectForm
            outlined
            class="row"
            :options="brandOptions"
            option_value="id"
            option_label="name"
            label="Marca*"
            not_found_label="No hay marcas disponibles"
            @updateModel="
              (value) => {
                supply.brand = value;
              }
            "
            :rules="[val => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir marca"
              class="add-btn"
              @click="flags.newBrandState = true"
            />
          </div>
        </div>
        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newBrand"
              class="col"
              label="Marca*"
              :disable="flags.disableBrand"
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableBrand ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="flags.disableBrand = !flags.disableBrand"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="flags.newBrandState = false"
            />
          </div>
        </div>

        <div v-if="!flags.newTypeState" class="col">
          <SelectForm
            outlined
            class="row"
            :options="typeOptions"
            option_value="id"
            option_label="name"
            label="Tipo de insumo*"
            not_found_label="No hay tipos de insumos disponibles"
            @updateModel="
              (value) => {
                supply.type = value;
              }
            "
            :rules="[val => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir tipo de insumo"
              class="add-btn"
              @click="flags.newTypeState = true"
            />
          </div>
        </div>
        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newType"
              class="col"
              label="Tipo de insumo*"
              :disable="flags.disableType"
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableType ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="flags.disableType = !flags.disableType"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="flags.newTypeState = false"
            />
          </div>
        </div>

        <div v-if="!flags.newFormatState" class="col">
          <SelectForm
            outlined
            class="row"
            :options="formatOptions"
            option_value="id"
            option_label="name"
            label="Formato de insumo*"
            not_found_label="No hay formatos de insumos disponibles"
            @updateModel="
              (value) => {
                supply.format = value;
              }
            "
            :rules="[val => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir formato de insumo"
              class="add-btn"
              @click="flags.newFormatState = true"
            />
          </div>
        </div>
        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newFormat"
              class="col"
              label="Tipo de insumo*"
              :disable="flags.disableFormat"
              :rules="[val => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableFormat ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="flags.disableFormat = !flags.disableFormat"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="flags.newFormatState = false"
            />
          </div>
        </div>
        <q-input
          outlined
          v-model="supply.observation"
          type="textarea"
          label="Observación"
          :rules="[val => !!val || 'Campo obligatorio']"
          lazy-rules
        />
        <!--Form button-->
        <div class="row justify-end q-mt-mx">
          <q-btn label="Crear" type="submit" color="positive" />
        </div>
        <q-inner-loading
          :showing="loading"
          label="Creando insumo"
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
import { ref, reactive, onMounted } from "vue";
import axios from "axios";
import SelectForm from "src/components/SelectForm.vue";

//Options Selects
const brandOptions = ref([]);
const formatOptions = ref([]);
const typeOptions = ref([]);

//Models
const supply = reactive({
  brand: null,
  type: null,
  name: null,
  code: null,
  format: null,
  samples: 0,
  lot_stock: 0,
  observation: null,
  critical_stock: 0,
});
const newBrand = ref(null);
const newFormat = ref(null);
const newType = ref(null);

//Flags
const flags = reactive({
  disableBrand: false,
  disableFormat: false,
  newBrandState: false,
  disableType: false,
  newTypeState: false,
  newFormatState: false,
});

const loading = ref(false);

//Form
const createSupplyForm = ref(null);
const router = useRouter();
const $q = useQuasar();
const api_prefix = process.env.API_URL;

const getSuppliesBrands = () => {
  axios.get(api_prefix + "/supplies_brands").then((response) => {
    const result = response.data;
    brandOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSuppliesFormats = () => {
  axios.get(api_prefix + "/supplies_formats").then((response) => {
    const result = response.data;
    formatOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSuppliesTypes = () => {
  axios.get(api_prefix + "/supplies_types").then((response) => {
    const result = response.data;
    typeOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

//Create functions

async function createNewBrand() {
  if (!flags.newBrandState) {
    return supply.brand;
  }
  const brandData = {
    name: newBrand.value,
  };

  try {
    const response = await axios.post(
      api_prefix + "/supplies_brands",
      brandData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la marca: " + error,
    });
  }
}

async function createNewFormat() {
  if (!flags.newFormatState) {
    return supply.format;
  }
  const formatData = {
    name: newFormat.value,
  };

  try {
    const response = await axios.post(
      api_prefix + "/supplies_formats",
      formatData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el formato: " + error,
    });
  }
}

async function createNewType() {
  if (!flags.newTypeState) {
    return supply.type;
  }
  const typeData = {
    name: newType.value,
  };

  try {
    const response = await axios.post(api_prefix + "/supplies_types", typeData);
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el tipo de insumo: " + error,
    });
  }
}

async function createNewSupply(supplyData) {
  try {
    const response = await axios.post(api_prefix + "/supplies", supplyData);
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el insumo: " + error,
    });
  }
}

async function onSubmit() {
  createSupplyForm.value.resetValidation();
  let supplyData = {
    name: supply.name,
    code: supply.code,
    stock: 0,
    critical_stock: supply.critical_stock,
    samples: supply.samples,
    lot_stock: supply.lot_stock,
    observation: supply.observation,
    supplies_brand_id: supply.brand,
    supplies_type_id: supply.type,
    supplies_format_id: supply.format
  };

  loading.value = true;

  const supplies_brand_id = await createNewBrand();
  if (supplies_brand_id == -1) {
    loading.value = false;
    return;
  }
  supplyData["supplies_brand_id"] = supplies_brand_id;

  const supplies_type_id = await createNewType();
  if (supplies_type_id == -1) {
    loading.value = false;
    return;
  }
  supplyData["supplies_type_id"] = supplies_type_id;

  const supplies_format_id = await createNewFormat();
  if (supplies_format_id == -1) {
    loading.value = false;
    return;
  }
  supplyData["supplies_format_id"] = supplies_format_id;

  const supply_id = await createNewSupply(supplyData);
  if (supply_id == -1) {
    loading.value = false;
    return;
  }
  loading.value = false;
  redirectToSupply(supply_id.toString());
  //Redirect to table
}

function redirectToSupply(supply_id) {
  router.push({ path: supply_id });
}

onMounted(() => {
  getSuppliesBrands();
  getSuppliesTypes();
  getSuppliesFormats();
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

.q-form {
  margin-top: 10px;
  background-color: #fffffe;
  border-radius: 1%;
  border-width: 1px;
  border-style: solid;
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
</style>
