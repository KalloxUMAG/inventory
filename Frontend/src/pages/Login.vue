<template>
  <q-card class="no-shadow">
    <q-card-section class="text-center">
      <div class="text-h4 text-weight-bold">
        Sistema de Inventario CADI UMAG
      </div>
    </q-card-section>
    <q-card-section class="q-mx-none">
      <q-form ref="loginForm" @submit.prevent="onSubmit">
        <div class="text-grey-8">Correo electrónico</div>
          <q-input v-model="email" dense outlined label="Correo electrónico">
            <template #prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
          <div class="text-grey-8 q-mt-md">Contraseña</div>
          <InputPassword
            autocomplete="current-password"
            v-model="password"
            dense
            label="Contraseña"
            :rules="[(val) => !!val || 'Campo obligatorio']"
          />
          <q-btn
            style="border-radius: 8px"
            color="dark"
            rounded
            size="md"
            label="Iniciar sesion"
            no-caps
            class="full-width q-mt-lg"
            type="submit"
          />
      </q-form>
    </q-card-section>
  </q-card>
  <q-inner-loading
    :showing="loading"
    label="Iniciando sesion..."
    label-class="text-secondary"
    label-style="font-size: 1.6em"
  />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import InputPassword from 'src/components/form/inputs/InputPassword.vue';

const $q = useQuasar()

const api_prefix = process.env.API_URL
const email = ref('')
const password = ref('')

const loginForm = ref(null)
const loading = ref(false)

const router = useRouter()

async function onSubmit() {
  loginForm.value.resetValidation()
  loading.value = true
  const data = {
    email: email.value,
    password: password.value,
  }
  try {
    const response = await axios.post(`${api_prefix}/users/login`, data)
    $q.cookies.set('CATGInventoryToken', response.data.access_token)
    $q.cookies.set('CATGInventoryFullname', response.data.fullname)
    loading.value = false
    router.push({ path: '/' })
  }
  catch (error) {
    loading.value = false
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo inicar sesion: ${error.response.data.detail}`,
      progress: true,
    })
  }
}

async function clearToken() {
  $q.cookies.remove('CATGInventoryToken')
  $q.cookies.remove('CATGInventoryFullname')
}

onMounted(() => {
  clearToken()
})
</script>

<style lang="css" scoped></style>
