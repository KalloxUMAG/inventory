<template>
  <div class="row justify-center">
    <q-form
      ref="changePasswordForm"
      class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
      @submit.prevent="onSubmit"
    >
      <h5>Cambiar Contraseña</h5>
      <div class="row">
        <InputPassword
          autocomplete="current-password"
          v-model="password"
          label="Contraseña actual*"
          :icon="false"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <InputPassword
          autocomplete="new-password"
          v-model="newPassword"
          label="Nueva contraseña*"
          :icon="false"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <!-- Form button -->
      <div class="row justify-end q-mt-mx">
        <q-btn label="Cambiar contraseña" type="submit" color="positive" />
      </div>
      <q-inner-loading
        :showing="loading"
        label="Cambiando contraseña"
        label-class="text-deep-orange"
        label-style="font-size: 1.6em"
      />
    </q-form>
  </div>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'
import InputPassword from 'src/components/form/inputs/InputPassword.vue';

const password = ref('')
const newPassword = ref('')

const loading = ref(false)

const changePasswordForm = ref(null)
const api_prefix = process.env.API_URL
const $q = useQuasar()

async function changePassword(data) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/users/change-password`,
      data,
    })
    $q.notify({
      color: 'green-3',
      textColor: 'white',
      icon: 'check',
      message: 'Contraseña cambiada con exito ',
    })
    password.value = ''
    newPassword.value = ''
    return response.status
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message:
        `No se pudo cambiar la contraseña: ${error.response.data.detail}`,
    })
  }
}

async function onSubmit() {
  changePasswordForm.value.resetValidation()
  loading.value = true

  const data = {
    old_password: password.value,
    new_password: newPassword.value,
  }

  await changePassword(data)
  loading.value = false
}
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

hr {
  width: 20%;
  height: 2px;
  background-color: black;
}

.q-form {
  margin-top: 10px;
  background-color: #fffffe;
  border-radius: 1%;
  border-width: 1px;
  border-style: solid;
}

.section-title {
  text-align: center;
  font-weight: bold;
  font-size: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

.add-btn {
  background-color: #7b7bd2 !important;
  color: #fff;
  border: 2px solid #7777cf;
}
</style>
