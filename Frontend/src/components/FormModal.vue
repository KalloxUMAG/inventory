<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="createModalForm">
        <div class="text-bold text-subtitle1">{{ title }}</div>
        <div v-for="(field, index) in fields" v-bind:key="index">
          <q-input v-if="field.type == 'text' || field.type == 'date'" :type="field.type" stack-label :label="field.label" v-model="models[index]" :autogrow="field.autogrow" :rules="field.rules" lazy-rules/>
          <SelectForm v-if="field.type == 'select'" stack-label :options="field.options" :option_value="field.option_value" :option_label="field.option_label" :label="field.label" :not_found_label="field.not_found_label" @updateModel="(value) => (models[index] = value)"/>
        </div>
        <div>
          <q-btn color="primary" label="Agregar" type="submit" />
          <q-btn color="negative" label="Cancelar" @click="onDialogCancel" />
        </div>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent } from 'quasar'
import {onMounted, ref, toRefs} from "vue";
import SelectForm from './SelectForm.vue';

const props = defineProps({
  title: String,
  fields: Array
})

const {fields} = toRefs(props)

const models = ref([])
const createModalForm = ref(null)

onMounted( () => {
  models.value = fields.value.map(x => x.defaultvalue)
})

defineEmits([
  // REQUIRED; need to specify some events that your
  // component will emit through useDialogPluginComponent()
  ...useDialogPluginComponent.emits
])

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
// dialogRef      - Vue ref to be applied to QDialog
// onDialogHide   - Function to be used as handler for @hide on QDialog
// onDialogOK     - Function to call to settle dialog with "ok" outcome
//                    example: onDialogOK() - no payload
//                    example: onDialogOK({ /*...*/ }) - with payload
// onDialogCancel - Function to call to settle dialog with "cancel" outcome

// this is part of our example (so not required)
function onOKClick () {
  // on OK, it is REQUIRED to
  // call onDialogOK (with optional payload)
  createModalForm.value.resetValidation();
  onDialogOK(models.value)
  // or with payload: onDialogOK({ ... })
  // ...and it will also hide the dialog automatically
}
</script>
