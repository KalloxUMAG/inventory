<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form ref="EditEquipmentPurchaseForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1">
          Datos compra
        </div>
        <!-- Fields -->
        <SelectForm
          :options="supplierOptions"
          option_value="id"
          option_label="name"
          label="Proveedor"
          not_found_label="No hay proveedores disponibles"
          :default_value="supplier_value"
          @update-model="
            (value) => {
              supplier = value;
              getInvoices();
            }
          "
        />
        <q-input
          v-model="reception_date"
          type="date"
          label="Fecha de recepción*"
          stack-label
          lazy-rules
          :rules="[
            (val) => (val && val != null) || 'Este campo es obligatorio',
          ]"
        />
        <SelectForm
          :options="invoiceOptions"
          option_value="id"
          option_label="name"
          label="Número de factura"
          not_found_label="No hay facturas disponibles"
          :default_value="invoice_value"
          @update-model="
            (value) => {
              invoice = value;
            }
          "
        />
        <SelectForm
          :options="projectOptions"
          option_value="id"
          option_label="name"
          label="Proyecto"
          not_found_label="No hay proyectos disponibles"
          :default_value="project_value"
          @update-model="
            (value) => {
              project = value;
              getStages();
            }
          "
        />
        <SelectForm
          :options="stageOptions"
          option_value="id"
          option_label="name"
          label="Etapa"
          not_found_label="No hay etapas disponibles"
          :default_value="stage_value"
          @update-model="
            (value) => {
              stage = value;
            }
          "
        />
        <!-- Buttons -->
        <div class="q-mt-sm row justify-end">
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
import { onMounted, ref, toRefs } from 'vue'
import { sendRequest } from 'src/services/axios/instance'
import SelectForm from 'src/components/SelectForm.vue'

const props = defineProps({
  id: Number,
  supplier_value: Object,
  reception_date_value: String,
  invoice_value: Object,
  project_value: Object,
  stage_value: Object,
})

defineEmits([...useDialogPluginComponent.emits])

const $q = useQuasar()

const {
  id,
  supplier_value,
  reception_date_value,
  invoice_value,
  project_value,
  stage_value,
} = toRefs(props)

const supplier = ref(supplier_value.value.id)
const reception_date = ref(reception_date_value.value)
const invoice = ref(invoice_value.value.id)
const project = ref(project_value.value.id)
const stage = ref(stage_value.value.id)

const supplierOptions = ref([])
const invoiceOptions = ref([])
const projectOptions = ref([])
const stageOptions = ref([])

const EditEquipmentPurchaseForm = ref(null)

const api_prefix = process.env.API_URL

async function getSuppliers() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers`,
    })
    const suppliers = response.data
    supplierOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getInvoices() {
  if (supplier.value === null) {
    invoiceOptions.value = []
    invoice.value = null
  }
  else {
    try {
      const response = await sendRequest({
        method: 'GET',
        url: `${api_prefix}/invoices/supplier/${supplier.value}`,
      })
      const invoices = response.data
      invoiceOptions.value = invoices.map((x) => {
        return { id: x.id, name: x.number }
      })
    }
    catch (error) {}
  }
}

async function getProjects() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/projects`,
    })
    const projects = response.data
    projectOptions.value = projects.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getStages() {
  if (project.value === null) {
    stageOptions.value = []
    stage.value = null
  }
  else {
    try {
      const response = await sendRequest({
        method: 'GET',
        url: `${api_prefix}/stages/${project.value}`,
      })
      const stages = response.data
      stageOptions.value = stages.map((x) => {
        return { id: x.id, name: x.name }
      })
    }
    catch (error) {}
  }
}

onMounted(() => {
  getSuppliers()
  getInvoices()
  getProjects()
  getStages()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
  = useDialogPluginComponent()
async function onOKClick() {
  EditEquipmentPurchaseForm.value.resetValidation()
  const data = {
    id: props.id,
    supplier_id: supplier.value,
    reception_date: reception_date.value,
    invoice_id: invoice.value,
  }
  try {
    const response = await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/equipments/${data.id}`,
      data,
    })
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo guardar los cambios: ${error}`,
    })
    return
  }
  onDialogOK()
}
</script>
