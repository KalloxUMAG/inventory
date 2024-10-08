<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form ref="AddSupplierForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1 q-my-sm">
          Datos proveedor
        </div>
        <!-- Fields -->
        <div v-if="!newsupplierstate">
          <SelectForm
            outlined
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
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir proveedor"
              icon="add"
              class="add-btn text-caption"
              @click="newsupplierstate = !newsupplierstate"
            />
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input
              v-model="newsuppliername"
              outlined
              label="Nombre proveedor"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div>
            <q-input
              v-model="newsupplierrut"
              outlined
              label="Rut"
              mask="##.###.###-X"
              unmasked-value
              class="row q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              v-model="newsupplieraddress"
              outlined
              label="Dirección"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              v-model="workername1"
              outlined
              label="Nombre trabajador"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <SelectForm
              outlined
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              class="col q-my-sm"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="(value) => (workerrol1 = value)"
            />
          </div>
          <div class="row">
            <q-input
              v-model="workermail1"
              outlined
              type="email"
              label="Correo trabajador"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              v-model="workerphone1"
              outlined
              label="Telefono trabajador"
              mask="(+##) #####-####"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>

          <div class="row justify-end q-mt-sm">
            <q-btn
              v-if="disableSupplier"
              label="Editar"
              color="amber"
              class="q-mr-sm"
              @click="disableSupplier = false"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              class="q-mr-sm"
              @click="notEmptyFields() ? (disableSupplier = true) : ''"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (newsupplierstate = !newsupplierstate),
                (disableSupplier = false)
              "
            />
          </div>
        </div>
        <div class="row">
          <q-input
            v-model="cost"
            outlined
            type="number"
            label="Costo"
            class="col q-my-sm"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
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
import { sendRequest } from 'src/services/axios/instance.js'
import { useDialogPluginComponent, useQuasar } from 'quasar'
import { onMounted, ref, toRefs } from 'vue'
import SelectForm from 'src/components/form/inputs/SelectForm.vue'
import { rolOptions } from 'src/constants/columns.js'

const props = defineProps({
  supply_id: Number,
})

defineEmits([...useDialogPluginComponent.emits])

const cost = ref(0)

const disableSupplier = ref(false)

const newsuppliername = ref('')
const newsupplierrut = ref('')
const newsupplieraddress = ref('')

const supplier = ref(null)
const suppliersOptions = ref([])
const newsupplierstate = ref(false)

const workername1 = ref('')
const workerrol1 = ref('')
const workermail1 = ref('')
const workerphone1 = ref('')

const $q = useQuasar()

const { supply_id } = toRefs(props)
const AddSupplierForm = ref(null)
const api_prefix = process.env.API_URL

async function getSuppliers() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers`,
    })
    const suppliers = response.data
    suppliersOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

function notEmptyFields() {
  return (
    newsuppliername.value != ''
    && newsupplierrut.value != ''
    && newsupplieraddress.value != ''
    && workername1.value != ''
    && workerrol1.value != ''
    && workermail1.value != ''
    && workerphone1.value != ''
  )
}

async function createNewSupplier() {
  if (!newsupplierstate.value)
    return supplier.value

  const supplierdata = {
    name: newsuppliername.value,
    rut: newsupplierrut.value,
    city_address: newsupplieraddress.value,
  }
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/suppliers`,
      data: supplierdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el proveedor: ${error}`,
    })
  }
}

async function createNewWorker(supplier_id) {
  if (!newsupplierstate.value)
    return

  if (workername1.value != null) {
    const workerdata = {
      name: workername1.value,
      position: workerrol1.value,
      phone: workerphone1.value,
      email: workermail1.value,
      supplier_id,
    }
    try {
      const response = await sendRequest({
        method: 'POST',
        url: `${api_prefix}/suppliers_contacts`,
        data: workerdata,
      })
    }
    catch (error) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `No se pudo crear el contacto 1: ${error}`,
      })
    }
  }
}

onMounted(() => {
  getSuppliers()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
  = useDialogPluginComponent()

async function onOKClick() {
  AddSupplierForm.value.resetValidation()
  const supplier_id = await createNewSupplier()
  await createNewWorker(supplier_id)
  const data = {
    supplier_id,
    supply_id: props.supply_id,
    cost: cost.value,
  }
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/suppliers_supplies`,
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
