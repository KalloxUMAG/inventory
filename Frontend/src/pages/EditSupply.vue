<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form @submit="onOKClick" ref="EditSupplyForm">
        <div class="text-bold text-subtitle1 q-my-sm">Editar insumo</div>
        <!--Fields-->
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
              :rules="[
                (val) =>
                  (val.length != 0 && val != null) || 'Campo obligatorio',
              ]"
            />
            <q-input
              outlined
              v-model="supply.lot_stock"
              label="Stock por lote*"
              type="number"
              step="any"
              class="col"
              :rules="[
                (val) =>
                  (val.length != 0 && val != null) || 'Campo obligatorio',
              ]"
            />
          </div>
        </div>
        <div class="col">
          <div class="row">
            <q-input
              outlined
              v-model="supply.stock"
              label="Stock actual"
              type="number"
              class="col q-mr-md"
              :rules="[
                (val) =>
                  (val.length != 0 && val != null) || 'Campo obligatorio',
              ]"
            />
            <q-input
              outlined
              v-model="supply.critical_stock"
              label="Stock crítico*"
              type="number"
              class="col"
              :rules="[(val) => !!val || 'Campo obligatorio']"
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
            :default_value="props.brand"
            label="Marca*"
            not_found_label="No hay marcas disponibles"
            @updateModel="
              (value) => {
                supply.brand = value;
              }
            "
            :rules="[(val) => !!val || 'Campo obligatorio']"
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
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableBrand ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="
                newBrand != '' ? (flags.disableBrand = !flags.disableBrand) : ''
              "
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
            :default_value="props.type"
            label="Tipo de insumo*"
            not_found_label="No hay tipos de insumos disponibles"
            @updateModel="
              (value) => {
                supply.type = value;
              }
            "
            :rules="[(val) => !!val || 'Campo obligatorio']"
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
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableType ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="
                newType != '' ? (flags.disableType = !flags.disableType) : ''
              "
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
            :default_value="props.format"
            label="Formato de insumo*"
            not_found_label="No hay formatos de insumos disponibles"
            @updateModel="
              (value) => {
                supply.format = value;
              }
            "
            :rules="[(val) => !!val || 'Campo obligatorio']"
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
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="flags.disableFormat ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="
                newFormat != ''
                  ? (flags.disableFormat = !flags.disableFormat)
                  : ''
              "
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
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
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
      <q-inner-loading
        :showing="loading"
        label="Creando insumo"
        label-class="text-deep-orange"
        label-style="font-size: 1.6em"
      />
    </q-card>
  </q-dialog>
</template>

<script setup>
import axios from "axios";
import { useDialogPluginComponent, useQuasar } from "quasar";
import { onMounted, reactive, ref, toRefs } from "vue";
import { sendRequest } from "src/axios/instance";
import SelectForm from "src/components/SelectForm.vue";
const api_prefix = process.env.API_URL;

const props = defineProps({
  supply_id: Number,
  brand: Object,
  type: Object,
  name: String,
  code: String,
  format: Object,
  samples: Number,
  stock: Number,
  lot_stock: Number,
  observation: String,
  critical_stock: Number,
});

const EditSupplyForm = ref(null);

const $q = useQuasar();

//Options Selects
const brandOptions = ref([]);
const formatOptions = ref([]);
const typeOptions = ref([]);

//Models
const supply = reactive({
  brand: props.brand.id,
  type: props.type.id,
  name: props.name,
  code: props.code,
  format: props.format.id,
  samples: props.samples,
  stock: props.stock,
  lot_stock: props.lot_stock,
  observation: props.observation,
  critical_stock: props.critical_stock,
});
const newBrand = ref("");
const newFormat = ref("");
const newType = ref("");

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

const getSuppliesBrands = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies_brands",
    });
    const result = response.data;
    brandOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  } catch (error) {}
};

const getSuppliesFormats = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies_formats",
    });
    const result = response.data;
    formatOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  } catch (error) {}
};

const getSuppliesTypes = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies_types",
    });
    const result = response.data;
    typeOptions.value = result.map((x) => {
      return { id: x.id, name: x.name };
    });
  } catch (error) {}
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
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/supplies_brands",
      data: brandData,
    });
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
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/supplies_formats",
      data: formatData,
    });
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
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/supplies_types",
      data: typeData,
    });
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

async function editSupply(data) {
  try {
    const response = await sendRequest({
      method: "PUT",
      url: api_prefix + "/supplies/" + props.supply_id,
      data: data,
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo editar el insumo: " + error,
    });
    return -1;
  }
}

onMounted(() => {
  getSuppliesBrands();
  getSuppliesTypes();
  getSuppliesFormats();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

async function onOKClick() {
  EditSupplyForm.value.resetValidation();

  const data = {
    name: supply.name,
    code: supply.code,
    critical_stock: supply.critical_stock,
    state: true,
    samples: supply.samples,
    lot_stock: supply.lot_stock,
    stock: supply.stock,
    observation: supply.observation,
    supplies_brand_id: supply.brand,
    supplies_type_id: supply.type,
    supplies_format_id: supply.format,
  };

  loading.value = true;

  const supplies_brand_id = await createNewBrand();
  if (supplies_brand_id == -1) {
    loading.value = false;
    return;
  }
  data["supplies_brand_id"] = supplies_brand_id;

  const supplies_type_id = await createNewType();
  if (supplies_type_id == -1) {
    loading.value = false;
    return;
  }
  data["supplies_type_id"] = supplies_type_id;

  const supplies_format_id = await createNewFormat();
  if (supplies_format_id == -1) {
    loading.value = false;
    return;
  }
  data["supplies_format_id"] = supplies_format_id;

  await editSupply(data);

  loading.value = false;

  onDialogOK();
}
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.add-btn {
  background-color: #7b7bd2 !important;
  color: #fff;
  border: 2px solid #7777cf;
}
</style>
