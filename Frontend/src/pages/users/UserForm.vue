<template>
  <PageTitle title="Nuevo Usuario" icon="person_add" />
  <q-form
    ref="createUserForm"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    @submit.prevent="onSubmit"
  >
    <FormSection title="Datos personales">
      <div class="row">
        <q-input
          v-model="user.fullname"
          outlined
          label="Nombre completo*"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <q-input
          v-model="user.username"
          outlined
          label="Nombre de usuario*"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <q-input
          v-model="user.email"
          outlined
          type="email"
          label="Correo electronico*"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <InputPassword
          autocomplete="new-user-password"
          v-model="user.password"
          :icon="false"
          label="Contraseña*"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div v-if="group" class="row">
        <InputSelect
          outlined
          bg-color="white"
          :clearable="false"
          class="col q-mr-md"
          :default_value="group"
          :options="groupsOptions"
          option_value="id"
          option_label="name"
          label="Grupo"
          not_found_label="No hay grupos disponibles"
          @update-model="(value) => (user.group = value)"
        />
      </div>
      <div v-if="role" class="row">
        <InputSelect
          :clearable="false"
          class="col q-mr-md"
          :default_value="role"
          :options="rolesOptions"
          option_value="id"
          option_label="name"
          label="Rol"
          not_found_label="No hay roles disponibles"
          @update-model="(value) => (user.role = value)"
        />
      </div>
      <div class="row">
        <UploadImages
          label="Imagen del usuario"
          :max_files="1"
          :handle-add-images="handleAddImages"
          :handle-remove-images="handleRemoveImages"
        />
      </div>
    </FormSection>
    <!-- Form button -->
    <div class="row justify-end q-mt-mx">
      <q-btn label="Crear" type="submit" color="positive" />
    </div>
    <q-inner-loading
      :showing="loading"
      label="Creando usuario"
      label-class="text-deep-orange"
      label-style="font-size: 1.6em"
    />
  </q-form>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { sendRequest } from 'src/services/axios/instance.js'

import PageTitle from 'src/components/commons/PageTitle.vue'
import FormSection from 'src/components/form/FormSection.vue'
import UploadImages from 'src/components/UploadImages.vue'
import InputSelect from 'src/components/form/inputs/InputSelect.vue'
import InputPassword from 'src/components/form/inputs/InputPassword.vue'

import { getGroups, getGroupRoles, postUser, addUserGroupRole } from 'src/services'

const createUserForm = ref(null)
const api_prefix = process.env.API_URL
const $q = useQuasar()
const router = useRouter()

const user = reactive({
  fullname: '',
  username: '',
  email: '',
  password: '',
  images: [],
  group: null,
  role: null,
})
const groupsOptions = ref([])
const rolesOptions = ref([])
const group = ref(null)
const role = ref(null)

const loading = ref(false)

// Functions

async function getGroupsData() {
  groupsOptions.value = await getGroups()
  group.value = groupsOptions.value[0]
  user.group = group.value.id
}

async function getGroupRolesData() {
  rolesOptions.value = await getGroupRoles()
  role.value = rolesOptions.value[0]
  user.role = role.value.id
}

async function onSubmit() {
  createUserForm.value.resetValidation()
  loading.value = true
  const userData = {
    username: user.username,
    email: user.email,
    fullname: user.fullname,
    password: user.password,
    images: user.images,
  }
  const userId = await postUser(userData)
  if (!userId) {
    loading.value = false
    return
  }
  await uploadUserImage(userId)
  await addUserGroupRole(userId, user.group, user.role)
  loading.value = false
  router.push({ path: userId.toString() })
}

async function uploadUserImage(userId) {
  if (user.images.length === 0)
    return

  user.images.forEach(async (image) => {
    const formData = new FormData()
    formData.append('file', image)
    try {
      const response = await sendRequest({
        method: 'POST',
        url: `${api_prefix}/users/images/${userId}`,
        data: formData,
      })
    }
    catch (error) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `No se pudo guardar la imagen del usuario: ${error}`,
      })
    }
  })
}

function handleAddImages(files) {
  user.images.push(files[0])
}

function handleRemoveImages(files) {
  user.images = user.images.filter((value) => {
    return value !== files[0]
  })
}

onMounted(() => {
  getGroupsData()
  getGroupRolesData()
})
</script>

<style scoped>
</style>
