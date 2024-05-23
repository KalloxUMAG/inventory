<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form ref="deleteItemForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1">
          ¿Estás seguro que quieres eliminar el {{ title }}?
        </div>
        <!-- Buttons -->
        <div class="q-mt-sm row justify-end">
          <q-btn
            color="primary"
            label="Aceptar"
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
import { useDialogPluginComponent } from 'quasar'
import { onMounted, ref, toRefs } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'

const props = defineProps({
  title: String,
  type: String,
  id: Number,
})

defineEmits([...useDialogPluginComponent.emits])

const { id, title, type } = toRefs(props)

const deleteItemForm = ref(null)
const api_prefix = process.env.API_URL

onMounted(() => {
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel }
    = useDialogPluginComponent()
async function onOKClick() {
  deleteItemForm.value.resetValidation()
  const data = {
    id,
  }
  try {
    const response = await sendRequest({
      method: 'DELETE',
      url: `${api_prefix}/${type.value}/${id.value}`,
    })
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo eliminar por completo: ${error}`,
    })
    return
  }
  onDialogOK()
}
</script>
