<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="EditEquipmentLocationForm">
        <div class="text-bold text-subtitle1">Datos ubicación</div>
        <!--Fields-->
        <SelectForm
          :options="buildingOptions"
          option_value="id"
          option_label="name"
          label="Edificio"
          not_found_label="No hay edificios disponibles"
          :default_value="building_value"
          @updateModel="
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
          @updateModel="
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
          @updateModel="
            (value) => {
              room = value;
            }
          "
        />
        <!--Buttons-->
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
import axios from "axios";
import { useDialogPluginComponent, useQuasar } from "quasar";
import { onMounted, ref, toRefs } from "vue";
import SelectForm from "src/components/SelectForm.vue";

const $q = useQuasar();

const props = defineProps({
  id: Number,
  room_value: Object,
  unit_value: Object,
  building_value: Object,
});

const { id, room_value, unit_value, building_value } = toRefs(props);

const room = ref(room_value.value.id);
const unit = ref(unit_value.value.id);
const building = ref(building_value.value.id);
const roomOptions = ref([]);
const unitOptions = ref([]);
const buildingOptions = ref([]);
const EditEquipmentLocationForm = ref(null);
const api_prefix = process.env.API;

const getBuildings = () => {
  axios.get(api_prefix + "/buildings").then((response) => {
    const buildings = response.data;
    buildingOptions.value = buildings.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getUnits = () => {
  if (building.value === null) {
    unitOptions.value = [];
    unit.value = null;
    roomOptions.value = [];
    room.value = null;
  } else {
    axios.get(api_prefix + "/units/" + building.value).then((response) => {
      const units = response.data;
      unitOptions.value = units.map((x) => {
        return { id: x.id, name: x.name };
      });
    });
  }
};

const getRooms = () => {
  if (unit.value === null) {
    console.log("Entro aqui");
    roomOptions.value = [];
    room.value = null;
  } else {
    axios.get(api_prefix + "/rooms/" + unit.value).then((response) => {
      const rooms = response.data;
      roomOptions.value = rooms.map((x) => {
        return { id: x.id, name: x.name };
      });
    });
  }
};

onMounted(() => {
  getBuildings();
  getUnits();
  getRooms();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
// dialogRef      - Vue ref to be applied to QDialog
// onDialogHide   - Function to be used as handler for @hide on QDialog
// onDialogOK     - Function to call to settle dialog with "ok" outcome
//                    example: onDialogOK() - no payload
//                    example: onDialogOK({ /*...*/ }) - with payload
// onDialogCancel - Function to call to settle dialog with "cancel" outcome

// this is part of our example (so not required)
async function onOKClick() {
  // on OK, it is REQUIRED to
  // call onDialogOK (with optional payload)
  EditEquipmentLocationForm.value.resetValidation();
  const data = {
    id: props.id,
    room_id: room.value,
  };
  try {
    const response = await axios.put(
      api_prefix + "/equipments/" + data.id,
      data
    );
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo guardar los cambios: " + error,
    });
    return;
  }
  onDialogOK();
  // or with payload: onDialogOK({ ... })
  // ...and it will also hide the dialog automatically
}
</script>
