<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form ref="AddSupplierForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1 q-my-sm">
          Datos proveedor
        </div>
        <!-- Fields -->
        <div>
          <InputSelect
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
            <!--Redirect to create supplier page-->
            <q-btn
              label="Añadir proveedor"
              icon="add"
              class="add-btn text-caption"
              @click="addSupplier"
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
import { useRouter } from 'vue-router'
import InputSelect from 'src/components/form/inputs/InputSelect.vue'

const props = defineProps({
  supply_id: Number,
})

defineEmits([...useDialogPluginComponent.emits])

const router = useRouter()

const cost = ref(null)

const supplier = ref(null)
const suppliersOptions = ref([])

const $q = useQuasar()

const { supply_id } = toRefs(props)
const AddSupplierForm = ref(null)
const api_prefix = process.env.API_URL

function addSupplier() {
    router.push('/suppliers/new_supplier')
  }

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

onMounted(() => {
  getSuppliers()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
  = useDialogPluginComponent()

async function onOKClick() {
  AddSupplierForm.value.resetValidation()
  const data = {
    supplier_id: supplier.value,
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
