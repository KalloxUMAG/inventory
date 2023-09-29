<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent="onSubmit"
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
        ref="createUserForm"
      >
        <h5>Nuevo usuario</h5>
        <div class="row">
          <q-input
            outlined
            label="Nombre completo*"
            v-model="fullname"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            outlined
            label="Nombre de usuario*"
            v-model="username"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            outlined
            type="email"
            label="Correo electronico*"
            v-model="email"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            outlined
            type="password"
            label="Contraseña*"
            v-model="password"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <!--Form button-->
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
    </div>
  </q-page>
</template>

<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import { sendRequest } from "src/axios/instance.js";

const fullname = ref("");
const username = ref("");
const email = ref("");
const password = ref("");

const loading = ref(false);

const createUserForm = ref(null);
const api_prefix = process.env.API_URL;
const $q = useQuasar();

const createNewUser = async (data) => {
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/users",
      data: data,
    });
    return response.status;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el usuario: " + error,
    });
  }
};

const onSubmit = async () => {
  createUserForm.value.resetValidation();
  loading.value = true;

  const data = {
    username: username.value,
    email: email.value,
    fullname: fullname.value,
    password: password.value,
  };

  await createNewUser(data);
  loading.value = false;
};
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
