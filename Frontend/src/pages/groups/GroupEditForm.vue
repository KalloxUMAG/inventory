<template>
  <PageTitle title="Nuevo Grupo" icon="group" />
  <q-form
    ref="editGroupForm"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    @submit.prevent="onSubmit"
  >
    <FormSection title="Datos Generales">
      <div class="row">
        <q-input
          v-model="group.name"
          class="col"
          label="Nombre"
          outlined
          placeholder="Nombre del grupo"
        />
      </div>
      <div class="row">
        <q-input
          v-model="group.description"
          class="col"
          outlined
          type="textarea"
          label="Descripción"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          hint="Breve descripción que ayude a comprender los objetivos y funciones del grupo"
        />
      </div>
      <div class="row">
        <q-input
          v-model="group.otherNames"
          class="col"
          label="Otros nombres"
          outlined
          placeholder="Otros nombres"
          hint="Otros nombres que serviran para refirse al grupo, separados por punto y coma (;). Ejemplo: Nombre1; Nombre2; Nombre3"
        />
      </div>
      <div class="row">
        <UploadImages
          ref="uploaderComponent"
          label="Imagen de grupo"
          :max_files="1"
          :handle-add-images="handleAddImages"
          :handle-remove-images="handleRemoveImages"
        />
      </div>
    </FormSection>
    <!-- Form button -->
    <div class="row justify-end q-mt-mx">
      <q-btn icon="save" label="Guardar" type="submit" color="positive" />
    </div>
    <q-inner-loading
      :showing="loading"
      label="Creando equipamiento"
      label-class="text-deep-orange"
      label-style="font-size: 1.6em"
    />
  </q-form>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

import PageTitle from 'src/components/commons/PageTitle.vue'
import FormSection from 'src/components/Form/FormSection.vue'
import UploadImages from 'src/components/UploadImages.vue'
import { sendRequest } from 'src/services/axios/instance.js'

import { useQuasar } from 'quasar'

import { computed, onMounted, reactive, ref } from 'vue'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()
const loading = ref(false)
const api_prefix = process.env.API_URL
const id = computed(() => route.params.id)
const query_groups = `${api_prefix}/groups/${id.value}`
const img_url = `${api_prefix}/groups/image/`
const editGroupForm = ref(null)
const originalGroup = reactive({
  name: null,
  description: null,
  otherNames: null,
  images: [],
})
const group = reactive({
  name: null,
  description: null,
  otherNames: null,
  images: [],
})
const uploaderComponent = ref(null)

onMounted(() => {
  getGroup()
})

async function getGroup() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: query_groups,
    })
    group.name = response.data.name
    group.description = response.data.description
    group.otherNames = response.data.other_names.join('; ')
    // Copy the original group data
    originalGroup.name = group.name
    originalGroup.description = group.description
    originalGroup.otherNames = response.data.other_names
    getImages()
  }
  catch (error) {
    console.log(error)
  }
}

async function getImages() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: img_url + id.value,
    })
    const images = response.data
    images.forEach(async (image) => {
      const imageResponse = await sendRequest({
        method: 'GET',
        url: api_prefix.slice(0, -4) + image.path,
        responseType: 'blob',
      })
      const blob = await imageResponse.data
      const imageFile = new File([blob], image.name, { type: blob.type, __img: 'img', __key: image.name, __progress: 0, __progressLabel: '0.00%', __status: 'idle', __uploaded: 0 })
      uploaderComponent.value.addFiles([imageFile])
      originalGroup.images.push(imageFile)
    })
  }
  catch (error) {
    console.log(error)
  }
}

function handleAddImages(files) {
  group.images.push(files[0])
}

function handleRemoveImages(files) {
  group.images = group.images.filter((value) => {
    return value != files[0]
  })
}

// Form validation

async function onSubmit() {
  editGroupForm.value.resetValidation()
  loading.value = true
  const groupData = {
    id: id.value,
    name: group.name,
    description: group.description,
    other_names: group.otherNames
      ? group.otherNames.split(';').map(name => name.trim())
      : [],
  }
  await updateGroup(groupData)
  await uploadGroupImage(id.value)
  loading.value = false
  router.push({ path: `/groups/${id.value.toString()}` })
}

async function updateGroup(groupData) {
  try {
    const response = await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/groups`,
      data: groupData,
    })
    if (response.status == 201) {
      $q.notify({
        color: 'green-4',
        textColor: 'white',
        icon: 'check',
        message: 'Grupo editado con éxito',
      })
    }
    return response.data
  }
  catch (error) {
    if (error.response.status == 409) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `Ya existe un grupo con el nombre ${groupData.name}`,
        timeout: 10000,
      })
    }
    else {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `No se pudo editar el Grupo: ${error}`,
        timeout: 10000,
      })
    }
  }
}

async function uploadGroupImage(groupId) {
  // Check if the images are the same
  if ((group.images.length == 0 && originalGroup.images.length == 0) || group.images == originalGroup.images)
    return

  // Delete the old images
  if (originalGroup.images.length > 0) {
    originalGroup.images.forEach(async (image) => {
      const formData = new FormData()
      formData.append('file', image)
      try {
        const response = await sendRequest({
          method: 'DELETE',
          url: `${api_prefix}/groups/image/${groupId}`,
          data: formData,
        })
      }
      catch (error) {
        $q.notify({
          color: 'red-3',
          textColor: 'white',
          icon: 'error',
          message: `No se pudo eliminar la imagen del grupo: ${error}`,
        })
      }
    })
  }
  // Upload the new images
  if (group.images.length > 0) {
    group.images.forEach(async (image) => {
      const formData = new FormData()
      formData.append('file', image)
      try {
        const response = await sendRequest({
          method: 'POST',
          url: `${api_prefix}/groups/${groupId}`,
          data: formData,
        })
      }
      catch (error) {
        $q.notify({
          color: 'red-3',
          textColor: 'white',
          icon: 'error',
          message: `No se pudo guardar la imagen del grupo: ${error}`,
        })
      }
    })
  }
}
</script>

<style scoped>
.form-input {
  background-color: #fff;
  border: 1px solid #ced4da;
  border-radius: 12px;
  box-shadow: inset 0 1px 1px #00000013;
  color: #495057;
}
</style>
