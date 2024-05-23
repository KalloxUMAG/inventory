<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form ref="EditEquipmentLocationForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1">
          Datos ubicación
        </div>
        <!-- Fields -->
        <SelectForm
          :options="buildingOptions"
          option_value="id"
          option_label="name"
          label="Edificio"
          not_found_label="No hay edificios disponibles"
          :default_value="building_value"
          @update-model="
            (value) => {
              building = value;
              getUnits();
            }
          "
        />
        <SelectForm
          :options="unitOptions"
          option_value="id"
          option_label="name"
          label="Unidad"
          not_found_label="No hay unidades disponibles"
          :default_value="unit_value"
          @update-model="
            (value) => {
              unit = value;
              getRooms();
            }
          "
        />
        <SelectForm
          :options="roomOptions"
          option_value="id"
          option_label="name"
          label="Salas"
          not_found_label="No hay salas disponibles"
          :default_value="room_value"
          @update-model="
            (value) => {
              room = value;
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
import { sendRequest } from 'src/services/axios/instance.js'
import SelectForm from 'src/components/SelectForm.vue'

const props = defineProps({
  id: Number,
  room_value: Object,
  unit_value: Object,
  building_value: Object,
})

defineEmits([...useDialogPluginComponent.emits])

const $q = useQuasar()

const { id, room_value, unit_value, building_value } = toRefs(props)

const room = ref(room_value.value.id)
const unit = ref(unit_value.value.id)
const building = ref(building_value.value.id)
const roomOptions = ref([])
const unitOptions = ref([])
const buildingOptions = ref([])
const EditEquipmentLocationForm = ref(null)
const api_prefix = process.env.API_URL

async function getBuildings() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/buildings`,
    })
    const buildings = response.data
    buildingOptions.value = buildings.map((x) => {
      return { id: x.id, name: x.name }
    })
  }
  catch (error) {}
}

async function getUnits() {
  if (building.value === null) {
    unitOptions.value = []
    unit.value = null
    roomOptions.value = []
    room.value = null
  }
  else {
    try {
      const response = await sendRequest({
        method: 'GET',
        url: `${api_prefix}/units/${building.value}`,
      })
      const units = response.data
      unitOptions.value = units.map((x) => {
        return { id: x.id, name: x.name }
      })
    }
    catch (error) {}
  }
}

async function getRooms() {
  if (unit.value === null) {
    roomOptions.value = []
    room.value = null
  }
  else {
    try {
      const response = await sendRequest({
        method: 'GET',
        url: `${api_prefix}/rooms/${unit.value}`,
      })
      const rooms = response.data
      roomOptions.value = rooms.map((x) => {
        return { id: x.id, name: x.name }
      })
    }
    catch (error) {}
  }
}

onMounted(() => {
  getBuildings()
  getUnits()
  getRooms()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
  = useDialogPluginComponent()
async function onOKClick() {
  EditEquipmentLocationForm.value.resetValidation()
  const data = {
    id: props.id,
    room_id: room.value,
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
