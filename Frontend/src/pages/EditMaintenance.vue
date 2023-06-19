<template>
    <q-dialog ref="dialogRef" @hide="onDialogHide">
      <q-card class="q-dialog-plugin q-pa-md">
        <q-form @submit="onOKClick" ref="EditMaintenanceForm">
          <div class="text-bold text-subtitle1">Editar mantenimiento</div>
          <!--Fields-->
          <q-input type="date" stack-label label="fecha" v-model="date" rules="[(val) => (val && val != null)" lazy-rules/>
          <SelectForm
            :options="typeOptions"
            option_value="id"
            option_label="name"
            label="Tipo de mantenimiento"
            not_found_label="No hay tipos disponibles"
            :default_value="type"
            @updateModel="
              (value) => {
                type = value
              }
            "
          />
          <SelectForm
            :options="typeOptions"
            option_value="id"
            option_label="name"
            label="Estado de mantenimineto"
            not_found_label="No hay estados disponibles"
            :default_value="type"
            @updateModel="
              (value) => {
                type = value
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
    date_value: String,
    type_value: Object,
    typeOptions: Array
  });
  
  const { id, date_value, type_value, typeOptions } = toRefs(props);

  const EditMaintenanceForm = ref(null);
  const api_prefix = process.env.API;
  
  const date = ref(date_value);
  const type = ref(type_value)
  
  onMounted(() => {
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
  