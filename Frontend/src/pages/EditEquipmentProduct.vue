<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="EditEquipmentProductForm">
        <div class="text-bold text-subtitle1">Datos producto</div>
        <!--Fields-->
        <q-input
          type="text"
          stack-label
          label="Nombre"
          v-model="name"
          :rules="[
            (val) => (val && val != null) || 'Este campo es obligatorio',
          ]"
          lazy-rules
        />
        <q-input
          type="text"
          stack-label
          label="Codigo serial"
          v-model="serial_number"
          :rules="[
            (val) => (val && val.length > 0) || 'Este campo es obligatorio',
            (val) => (val && val.length < 256) || 'Máximo 255 caracteres',
          ]"
          lazy-rules
        />
        <q-input
          type="number"
          stack-label
          label="Inventario UMAG"
          v-model="umag_inventory_code"
          :rules="[
            (val) =>
              (val.length < 26 && val > 0) ||
              'El valor debe ser mayor que 0 y tener un maximo de 25 dígitos',
          ]"
          lazy-rules
        />
        <SelectForm
          :options="brandOptions"
          option_value="id"
          option_label="name"
          label="Marca"
          not_found_label="No hay marcas disponibles"
          :default_value="brand_value"
          @updateModel="
            (value) => {
              brand = value;
              getModels();
            }
          "
        />
        <SelectForm
          :options="modelOptions"
          option_value="id"
          option_label="name"
          label="Modelo"
          not_found_label="No hay modelos disponibles"
          :default_value="model_value"
          @updateModel="
            (value) => {
              model = value;
              getModelNumbers();
            }
          "
        />
        <SelectForm
          :options="modelNumberOptions"
          option_value="id"
          option_label="name"
          label="Numero Modelo"
          not_found_label="No hay numeros de modelo disponibles"
          :default_value="model_number_value"
          @updateModel="
            (value) => {
              model_number = value;
            }
          "
        />
        <q-input
          type="text"
          stack-label
          label="Observacion"
          v-model="observation"
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
      {{ brand }}
      {{ modelOptions }}
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
  name_value: String,
  serial_number_value: String,
  umag_inventory_code_value: Number,
  model_value: Object,
  brand_value: Number,
  model_number_value: String,
  maintenance_period_value: Number,
  observation_value: String,
});
const maintenanceOptions = [
  {
    id: 1,
    name: "Mensual",
  },
  {
    id: 3,
    name: "Trimestral",
  },
  {
    id: 6,
    name: "Semestral",
  },
  {
    id: 12,
    name: "Anual",
  },
  {
    id: null,
    name: "No aplica",
  },
];

const {
  id,
  name_value,
  serial_number_value,
  umag_inventory_code_value,
  model_value,
  brand_value,
  model_number_value,
  maintenance_period_value,
  observation_value,
} = toRefs(props);

const name = ref(name_value.value);
const serial_number = ref(serial_number_value.value);
const umag_inventory_code = ref(umag_inventory_code_value.value);
const brand = ref(brand_value.value.id);
const model = ref(model_value.value.id);
const modelOptions = ref([]);
const brandOptions = ref([]);
const model_number = ref(model_number_value.value.id);
const modelNumberOptions = ref([]);
const maintenance_period = ref(maintenance_period_value.value);
const observation = ref(observation_value.value);
const EditEquipmentProductForm = ref(null);
const api_prefix = process.env.API;

const getBrands = () => {
  axios.get(api_prefix + "/brands").then((response) => {
    const brands = response.data;
    brandOptions.value = brands.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getModels = () => {
  if (brand.value === null) {
    modelOptions.value = [];
    model.value = null;
    modelNumberOptions.value = [];
    model_number.value = null;
  } else {
    axios.get(api_prefix + "/models/" + brand.value).then((response) => {
      const models = response.data;
      modelOptions.value = models.map((x) => {
        return { id: x.id, name: x.name };
      });
    });
  }
};

const getModelNumbers = () => {
  if (model.value === null) {
    modelNumberOptions.value = [];
    model_number.value = null;
  } else {
    axios.get(api_prefix + "/model_numbers/" + model.value).then((response) => {
      const modelnumbers = response.data;
      modelNumberOptions.value = modelnumbers.map((x) => {
        return { id: x.id, name: x.number };
      });
    });
  }
};

onMounted(() => {
  getBrands();
  getModels();
  getModelNumbers();
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
  EditEquipmentProductForm.value.resetValidation();
  const data = {
    id: props.id,
    name: name.value,
    serial_number: serial_number.value,
    umag_inventory_code: umag_inventory_code.value,
    observation: observation.value,
    model_number_id: model_number.value,
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
