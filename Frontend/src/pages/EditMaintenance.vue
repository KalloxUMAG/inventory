<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="EditMaintenanceForm">
        <div class="text-bold text-subtitle1">Editar mantenimiento</div>
        <!--Fields-->
        <q-input
          type="date"
          stack-label
          label="fecha"
          v-model="date"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
        <SelectForm
          :options="typeOptions"
          option_value="id"
          option_label="name"
          label="Tipo de mantenimiento"
          not_found_label="No hay tipos disponibles"
          :default_value="type_value"
          @updateModel="
            (value) => {
              type = value;
            }
          "
        />
        <SelectForm
          :options="stateOptions"
          option_value="id"
          option_label="name"
          label="Estado de mantenimiento"
          not_found_label="No hay estados disponibles"
          :default_value="state_value"
          @updateModel="
            (value) => {
              state = value;
            }
          "
        />
        <q-input v-model="observation" label="Observacion" autogrow="" />
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
import { sendRequest } from "src/axios/instance";
import SelectForm from "src/components/SelectForm.vue";

const $q = useQuasar();

const props = defineProps({
  id: Number,
  date_value: String,
  type_value: Object,
  typeOptions: Array,
  state_value: Object,
  stateOptions: Array,
  observation_value: String,
  equiptment_id: Number,
});

const {
  id,
  date_value,
  type_value,
  typeOptions,
  state_value,
  stateOptions,
  observation_value,
  equiptment_id,
} = toRefs(props);

const EditMaintenanceForm = ref(null);
const api_prefix = process.env.API_URL;

const date = ref(date_value.value);
const type = ref(type_value.value.id);
const state = ref(state_value.value.id);
const observation = ref(observation_value.value);

onMounted(() => {});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
async function onOKClick() {
  EditMaintenanceForm.value.resetValidation();
  const newState = state.value == 0 ? false : true;
  const data = {
    date: date.value,
    observations: observation.value,
    state: newState,
    maintenance_type: type.value,
  };

  if (id.value == null) {
    data["equiptment_id"] = equiptment_id.value;
    try {
      const response = await sendRequest({
        method: "POST",
        url: api_prefix + "/maintenances",
        data: data,
      });
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo guardar los cambios: " + error,
      });
      return;
    }
  } else {
    try {
      const response = await sendRequest({
        method: "PUT",
        url: api_prefix + "/maintenances/" + id.value,
        data: data,
      });
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo guardar los cambios: " + error,
      });
      return;
    }
  }
  onDialogOK();
}
</script>
