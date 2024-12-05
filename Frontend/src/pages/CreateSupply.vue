<template>
  <PageTitle title="Nuevo insumo" />
  <q-form
    ref="createSupplyForm"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    @submit.prevent="onSubmit"
  >
    <!-- Datos Producto -->
    <FormSection title="Datos insumo">
      <div class="col">
        <div class="row">
          <q-input
            v-model="supply.name"
            outlined
            label="Nombre*"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <q-input
            v-model="supply.code"
            outlined
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
            v-model="supply.samples"
            outlined
            label="Muestras por unidad*"
            type="number"
            step="any"
            class="col q-mr-md"
            :rules="[
              (val) => (val.length > 0 && val != null) || 'Campo obligatorio',
            ]"
          />
          <q-input
            v-model="supply.lot_stock"
            outlined
            label="Stock por lote*"
            type="number"
            step="any"
            class="col"
            :rules="[
              (val) => (val.length > 0 && val != null) || 'Campo obligatorio',
            ]"
          />
        </div>
      </div>
      <div class="col">
        <div class="row">
          <q-input
            v-model="supply.critical_stock"
            outlined
            label="Stock crítico*"
            type="number"
            class="col"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
      </div>
      <div v-if="!flags.newBrandState" class="col">
        <InputSelect
          outlined
          class="row"
          :options="brandOptions"
          option_value="id"
          option_label="name"
          label="Marca*"
          not_found_label="No hay marcas disponibles"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          @update-model="
            (value) => {
              supply.brand = value;
            }
          "
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
            v-model="newBrand"
            outlined
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

      <div class="col">
        <InputSelect
          outlined
          class="row"
          :options="typeOptions"
          option_value="id"
          option_label="name"
          label="Tipo de insumo*"
          not_found_label="No hay tipos de insumos disponibles"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          @update-model="
            (value) => {
              supply.type = value;
            }
          "
        />
      </div>

      <div v-if="!flags.newFormatState" class="col">
        <InputSelect
          outlined
          class="row"
          :options="formatOptions"
          option_value="id"
          option_label="name"
          label="Formato de insumo*"
          not_found_label="No hay formatos de insumos disponibles"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          @update-model="
            (value) => {
              supply.format = value;
            }
          "
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
            v-model="newFormat"
            outlined
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
      <div class="row">
        <InputSelect
          outlined
          class="col q-mb-lg"
          :options="temperatureOptions"
          option_value="id"
          option_label="name"
          label="Temperatura de almacenamiento"
          not_found_label="No hay temperaturas disponibles"
          @update-model="
            (value) => {
              supply.temperature = value;
            }
          "/>
      </div>
      <q-input
        v-model="supply.observation"
        outlined
        type="textarea"
        label="Observación"
        lazy-rules
      />
    </FormSection>
    <!-- Form button -->
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
</template>

<script setup>
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { onMounted, reactive, ref } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'
import InputSelect from 'src/components/form/inputs/InputSelect.vue'
import FormSection from 'src/components/form/FormSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

// Options Selects
const brandOptions = ref([])
const formatOptions = ref([])
const typeOptions = ref([])

// Models
const supply = reactive({
  brand: null,
  type: null,
  name: null,
  code: null,
  format: null,
  samples: 0,
  lot_stock: 0,
  observation: "",
  temperature: null,
  critical_stock: 0,
})
const newBrand = ref('')
const newFormat = ref('')
const newType = ref('')

// Flags
const flags = reactive({
  disableBrand: false,
  disableFormat: false,
  newBrandState: false,
  disableType: false,
  newFormatState: false,
})

const loading = ref(false)

const temperatureOptions = [
  { id: 'Ambiente', name: 'Ambiente' },
  { id: '4 grados Celsius', name: '4 grados Celsius' },
  { id: '-20 Grados Celsius', name: '-20 Grados Celsius' },
  { id: '-80 Grados Celsius', name: '-80 Grados Celsius' }
]

// Form
const createSupplyForm = ref(null)
const router = useRouter()
const $q = useQuasar()
const api_prefix = process.env.API_URL

async function getSuppliesBrands() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies_brands`,
    })
    const result = response.data
    brandOptions.value = result.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getSuppliesFormats() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies_formats`,
    })
    const result = response.data
    formatOptions.value = result.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getSuppliesTypes() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies_types`,
    })
    const result = response.data
    typeOptions.value = result.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

// Create functions

async function createNewBrand() {
  if (!flags.newBrandState)
    return supply.brand

  const brandData = {
    name: newBrand.value,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/supplies_brands`,
      data: brandData,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la marca: ${error}`,
    })
  }
}

async function createNewFormat() {
  if (!flags.newFormatState)
    return supply.format

  const formatData = {
    name: newFormat.value,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/supplies_formats`,
      data: formatData,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el formato: ${error}`,
    })
  }
}

async function createNewSupply(supplyData) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/supplies`,
      data: supplyData,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el insumo: ${error}`,
    })
  }
}

async function onSubmit() {
  createSupplyForm.value.resetValidation()
  const supplyData = {
    name: supply.name,
    code: supply.code,
    stock: 0,
    critical_stock: supply.critical_stock,
    samples: supply.samples,
    lot_stock: supply.lot_stock,
    observation: supply.observation,
    temperature: supply.temperature,
    supplies_brand_id: supply.brand,
    supplies_type_id: supply.type,
    supplies_format_id: supply.format,
  }

  loading.value = true

  const supplies_brand_id = await createNewBrand()
  if (supplies_brand_id == -1) {
    loading.value = false
    return
  }
  supplyData.supplies_brand_id = supplies_brand_id

  const supplies_type_id = supply.type
  supplyData.supplies_type_id = supplies_type_id

  const supplies_format_id = await createNewFormat()
  if (supplies_format_id == -1) {
    loading.value = false
    return
  }
  supplyData.supplies_format_id = supplies_format_id

  const supply_id = await createNewSupply(supplyData)
  if (supply_id == -1) {
    loading.value = false
    return
  }
  loading.value = false
  redirectToSupply(supply_id.toString())
  // Redirect to table
}

function redirectToSupply(supply_id) {
  router.push({ path: supply_id })
}

onMounted(() => {
  getSuppliesBrands()
  getSuppliesTypes()
  getSuppliesFormats()
})
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
</style>
