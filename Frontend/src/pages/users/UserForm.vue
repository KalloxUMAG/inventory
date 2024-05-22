<template>
  <PageTitle title="Nuevo Usuario" icon="person_add" />
  <q-form
    @submit.prevent="onSubmit"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    ref="createUserForm"
  >
    <FormSection title="Datos personales">
      <div class="row">
        <q-input
          outlined
          label="Nombre completo*"
          v-model="user.fullname"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <q-input
          outlined
          label="Nombre de usuario*"
          v-model="user.username"
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
          v-model="user.email"
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
          v-model="user.password"
          class="col q-mr-md"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
        />
      </div>
      <div class="row">
        <UploadImages
          label="Imagen del usuario"
          :max_files="1"
          :handleAddImages="handleAddImages"
          :handleRemoveImages="handleRemoveImages"
        />
      </div>
    </FormSection>
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
</template>

<script setup>
import { useQuasar } from "quasar";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance.js";

import PageTitle from "src/components/commons/PageTitle.vue";
import FormSection from "src/components/Form/FormSection.vue";
import UploadImages from "src/components/UploadImages.vue";

const createUserForm = ref(null);
const api_prefix = process.env.API_URL;
const $q = useQuasar();
const router = useRouter();

const user = reactive({
  fullname: "",
  username: "",
  email: "",
  password: "",
  images: [],
});

const loading = ref(false);

//Functions

const onSubmit = async () => {
  createUserForm.value.resetValidation();
  loading.value = true;
  let userData = {
    username: user.username,
    email: user.email,
    fullname: user.fullname,
    password: user.password,
    images: user.images,
  };
  console.log(userData);
  const userId = await createNewUser(userData);
  await uploadUserImage(userId);
  loading.value = false;
  router.push({ path: userId.toString() });
};

const createNewUser = async (data) => {
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/users",
      data: data,
    });
    $q.notify({
      color: "green-3",
      textColor: "white",
      icon: "check",
      message: "Usuario creado con exito ",
    });
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el usuario: " + error.response.data.detail,
    });
  }
};

const uploadUserImage = async (userId) => {
  if (user.images.length == 0) {
    return;
  }
  user.images.forEach(async (image) => {
    const formData = new FormData();
    formData.append("file", image);
    try {
      const response = await sendRequest({
        method: "POST",
        url: api_prefix + "/users/images/" + userId,
        data: formData,
      });
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo guardar la imagen del usuario: " + error,
      });
    }
  });
};

const handleAddImages = (files) => {
  user.images.push(files[0]);
};

const handleRemoveImages = (files) => {
  user.images = user.images.filter((value) => {
    return value != files[0];
  });
};
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
