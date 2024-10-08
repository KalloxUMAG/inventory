<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md" style="width: 900px; max-width: 1000px;">
      <q-card-section>
        <h3 class="text-bold text-h5 q-my-sm">
          Datos del prestamo
        </h3>
        <p class="text-grey-7">
          Preste el lote de un grupo (El lote será consumido)
        </p>
        <q-separator />
      </q-card-section>
      <q-card-section>
        <q-form ref="EditLoanForm" @submit="onOKClick">
          <div class="row q-col-gutter-md">
            <q-input
              v-model="group"
              label="Grupo que presta"
              outlined
              class="col-12"
              hint="El grupo que presta el lote"
              readonly
            />
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <q-input
              v-model="supply"
              label="Insumo a prestar"
              outlined
              class="col-12 col-md-6"
              hint="El insumo que se presta"
              readonly
            />
            <q-input
              v-model="lot"
              label="Lote a prestar"
              outlined
              class="col-12 col-md-6"
              hint="El lote que se presta (Se consumirá)"
              readonly
            />
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <q-input
              v-model="loanDate"
              type="date"
              label="Fecha de prestamo"
              outlined
              class="col-12 col-md-6"
              :rules="[val => !!val || 'Ingrese una fecha']"
              hint="Fecha en que se hace efectivo el prestamo"
            />
            <q-input
              v-model="returnDate"
              type="date"
              label="Fecha de devolución"
              outlined
              class="col-12 col-md-6"
              hint="Fecha en que se devolverá/devolvio el lote"
            />
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <SelectForm
              v-model="status"
              label="Estado"
              outlined
              class="col-12"
              :options="statusOptions"
              option_value="value"
              option_label="label"
              not_found_label="No hay estados"
              :rules="[val => !!val || 'Seleccione un estado']"
              hint="Estado del prestamo"
              @update-model="(value) => { status = value }"
            />
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <q-input
              v-model="description"
              type="textarea"
              label="Descripción"
              outlined
              class="col-12"
              hint="Describa a quien se presta el lote y como contactarlo"
              :rules="[val => !!val || 'Ingrese una descripción']"
            />
          </div>
          <q-card-actions align="right" class="q-mt-md">
            <q-btn
              label="Guardar"
              color="primary"
              @click="onOKClick"
            />
            <q-btn
              label="Cancelar"
              color="negative"
              @click="onDialogCancel"
            />
          </q-card-actions>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent } from 'quasar'
import { onMounted, ref } from 'vue'
import { putLoan } from 'src/services'
import SelectForm from 'src/components/form/inputs/SelectForm.vue'

const props = defineProps({
  id: Number,
  group: String,
  supply: String,
  lot: String,
  loanDate: String,
  returnDate: String,
  state: String,
  description: String,
})

defineEmits([...useDialogPluginComponent.emits])

// Form data
const group = ref(props.group)
const supply = ref(props.supply)
const lot = ref(props.lot)
const loanDate = ref(props.loanDate)
const returnDate = ref(props.returnDate)
const status = ref(props.state)
const description = ref(props.description)

// Data
const statusOptions = ref([
  { label: 'Pendiente', value: 'pendiente' },
  { label: 'Devuelto', value: 'devuelto' },
])

const EditLoanForm = ref(null)

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()

async function onOKClick() {
  await putLoan(props.id, {
    start_date: loanDate.value,
    end_date: returnDate.value,
    state: status.value,
    description: description.value,
  })
  onDialogOK()
}

onMounted(() => {
})
</script>
