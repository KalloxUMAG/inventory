<template>
  <q-form ref="loginForm" @submit.prevent="onSubmit">
    <q-card class="q-pa-md shadow-2 my_card" bordered>
      <q-card-section class="text-center">
        <div class="text-h4 text-weight-bold">
          Sistema de Gestion de Inventario CADI
        </div>
      </q-card-section>
      <q-card-section class="text-center">
        <div class="text-grey-9 text-h5 text-weight-bold">Iniciar sesion</div>
      </q-card-section>
      <q-card-section>
        <q-input dense outlined v-model="email" label="Correo">
          <template v-slot:prepend>
            <q-icon name="mail" />
          </template>
        </q-input>
        <q-input
          dense
          outlined
          icon
          class="q-mt-md"
          v-model="password"
          type="password"
          label="Contrasena"
        >
          <template v-slot:prepend>
            <q-icon name="key" />
          </template>
        </q-input>
      </q-card-section>
      <q-card-section>
        <q-btn
          style="border-radius: 8px"
          color="dark"
          rounded
          size="md"
          label="Iniciar sesion"
          no-caps
          class="full-width"
          type="submit"
        ></q-btn>
      </q-card-section>
    </q-card>
  </q-form>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useQuasar } from "quasar";
import { useRouter } from "vue-router";

const $q = useQuasar();

const api_prefix = process.env.API_URL;
const email = ref("");
const password = ref("");

const loginForm = ref(null);

const router = useRouter();

const onSubmit = async () => {
  loginForm.value.resetValidation();
  const data = {
    email: email.value,
    password: password.value,
  };
  try {
    const response = await axios.post(api_prefix + "/users/login", data);
    $q.localStorage.set("CATGInventoryToken", response.data.access_token);
    $q.localStorage.set("CATGInventoryFullname", response.data.fullname);
    router.push({ path: "/" });
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo inicar sesion: " + error.response.data.detail,
      progress: true,
    });
  }
};

async function clearToken() {
  $q.localStorage.remove("CATGInventoryToken");
  $q.localStorage.remove("CATGInventoryFullname");
}

onMounted(() => {
  clearToken();
});
</script>

<style lang="css" scoped></style>
