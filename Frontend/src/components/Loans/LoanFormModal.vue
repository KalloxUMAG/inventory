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
        <q-form ref="AddLoanForm" @submit="onOKClick">
          <div class="row q-col-gutter-md">
            <SelectForm
              v-model="group"
              label="Grupo que presta"
              outlined
              class="col-12"
              :options="groups"
              option_value="id"
              option_label="name"
              not_found_label="No hay grupos"
              :rules="[val => !!val || 'Seleccione un grupo']"
              hint="El grupo que presta el lote"
              @update-model="(value) => { group = value; loadSupplies(value) }"
            />
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <SelectForm
              v-model="supply"
              label="Insumo a prestar"
              outlined
              class="col-12 col-md-6"
              :options="supplies"
              option_value="id"
              option_label="name"
              not_found_label="No hay insumos"
              :rules="[val => !!val || 'Seleccione un insumo']"
              hint="El insumo que se presta"
              @update-model="(value) => { supply = value; loadLots(value) }"
            />
            <SelectForm
              v-model="lot"
              label="Lote a prestar"
              outlined
              class="col-12 col-md-6"
              :options="lots"
              option_value="id"
              option_label="name"
              not_found_label="No hay lotes"
              :rules="[val => !!val || 'Seleccione un lote']"
              hint="El lote que se presta (Se consumirá)"
              @update-model="(value) => { lot = value }"
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
import { getGroups, getLotsBySupplyId, getSuppliesByGroupId, postLoan } from 'src/services'
import SelectForm from '../SelectForm.vue'

defineEmits([...useDialogPluginComponent.emits])

// Form data
const group = ref(null)
const supply = ref(null)
const lot = ref(null)
const loanDate = ref(null)
const returnDate = ref(null)
const status = ref(null)
const description = ref(null)

// Data
const groups = ref([])
const supplies = ref([])
const lots = ref([])
const statusOptions = ref([
  { label: 'Pendiente', value: 'pendiente' },
  { label: 'Devuelto', value: 'devuelto' },
])

const AddLoanForm = ref(null)

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()

async function onOKClick() {
  await postLoan({
    lot_id: lot.value,
    start_date: loanDate.value,
    end_date: returnDate.value,
    state: status.value,
    description: description.value,
  })
  onDialogOK()
}

async function loadGroups() {
  groups.value = await getGroups()
}

async function loadSupplies(group_id) {
  if (!group_id) {
    supplies.value = []
    supply.value = null
    lots.value = []
    lot.value = null
    return
  }
  const data = await getSuppliesByGroupId(group_id)
  supplies.value = data.map((supply) => {
    return {
      id: supply.id,
      name: `${supply.name} | ${supply.code}`,
    }
  })
}

async function loadLots(supply_id) {
  if (!supply_id) {
    lots.value = []
    lot.value = null
    return
  }
  const data = await getLotsBySupplyId(supply_id)
  lots.value = data.map((lot) => {
    return {
      id: lot.id,
      name: `N°: ${lot.number} | Stock:${lot.stock}`,
    }
  })
}

onMounted(() => {
  loadGroups()
})
</script>
