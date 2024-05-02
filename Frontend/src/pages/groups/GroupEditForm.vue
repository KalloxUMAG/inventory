<template>
  <PageTitle title="Nuevo Grupo" icon="group" />
  <q-form
    @submit.prevent="onSubmit"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    ref="createGroupForm"
  >
    <FormSection title="Datos Generales">
      <div class="row">
        <q-input
          class="col"
          v-model="group.name"
          label="Nombre"
          outlined
          placeholder="Nombre del grupo"
        />
      </div>
      <div class="row">
        <q-input
          class="col"
          outlined
          v-model="group.description"
          type="textarea"
          label="Descripción"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          hint="Breve descripción que ayude a comprender los objetivos y funciones del grupo"
        />
      </div>
      <div class="row">
        <q-input
          class="col"
          v-model="group.otherNames"
          label="Otros nombres"
          outlined
          placeholder="Otros nombres"
          hint="Otros nombres que serviran para refirse al grupo, separados por punto y coma (;). Ejemplo: Nombre1; Nombre2; Nombre3"
        />
      </div>
      <div class="row">
        <UploadImages
          label="Imagen de grupo"
          :max_files="1"
          :handleAddImages="handleAddImages"
          :handleRemoveImages="handleRemoveImages"
          ref="uploaderComponent"
        />
      </div>
    </FormSection>
    <!--Form button-->
    <div class="row justify-end q-mt-mx">
      <q-btn icon="add" label="Crear" type="submit" color="positive" />
    </div>
  </q-form>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";

import PageTitle from "src/components/commons/PageTitle.vue";
import FormSection from "src/components/Form/FormSection.vue";
import UploadImages from "src/components/UploadImages.vue";
import { sendRequest } from "src/axios/instance.js";

import { useQuasar } from "quasar";

import { ref, reactive, onMounted, computed } from "vue";

const $q = useQuasar();
const route = useRoute();
const router = useRouter();
const api_prefix = process.env.API_URL;
const id = computed(() => route.params.id);
const query_groups = api_prefix + "/groups/" + id.value;
const img_url = api_prefix + "/groups/image/";
const createGroupForm = ref(null);
const group = reactive({
  name: null,
  description: null,
  otherNames: null,
  images: [],
});
const uploaderComponent = ref(null);

onMounted(() => {
  getGroup();
});

const getGroup = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: query_groups,
    });
    group.name = response.data.name;
    group.description = response.data.description;
    group.otherNames = response.data.other_names.join("; ");
    getImages();
  } catch (error) {
    console.log(error);
  }
};

const getImages = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: img_url + id.value,
    });
    const images = response.data;
    images.forEach(async(image) => {
      const imageResponse = await sendRequest({
          method: "GET",
          url: api_prefix.slice(0, -4) + image.path,
          responseType: "blob",
      });
      const blob = await imageResponse.data;
      const imageFile = new File([blob], image.name, {type: blob.type, __img: 'img', __key: image.name, __progress: 0, __progressLabel: '0.00%', __status: 'idle', __uploaded: 0});
      uploaderComponent.value.addFiles([imageFile]);
    });
  } catch (error) {
    console.log(error);
  }
};

const handleAddImages = (files) => {
  group.images.push(files[0]);
};

const handleRemoveImages = (files) => {
  group.images = group.images.filter((value) => {
    return value != files[0];
  });
};

// Form validation

const onSubmit = async () => {
  createGroupForm.value.resetValidation();
  let groupData = {
    name: group.name,
    description: group.description,
    other_names: group.otherNames
      ? group.otherNames.split(";").map((name) => name.trim())
      : [],
    images: group.images,
  };
  const groupId = await createNewGroup(groupData);
  await uploadGroupImage(groupId);
  router.push({ path: groupId.toString() });
};

const createNewGroup = async (groupData) => {
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/groups",
      data: groupData,
    });
    if (response.status == 201) {
      $q.notify({
        color: "green-4",
        textColor: "white",
        icon: "check",
        message: "Grupo creado con éxito",
      });
    }
    return response.data;
  } catch (error) {
    if (error.response.status == 409) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "Ya existe un grupo con el nombre " + groupData.name,
        timeout: 10000,
      });
    } else {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el Grupo: " + error,
        timeout: 10000,
      });
    }
  }
};

const uploadGroupImage = async (groupId) => {
  if (group.images.length == 0) {
    return;
  }
  group.images.forEach(async (image) => {
    const formData = new FormData();
    formData.append("file", image);
    try {
      const response = await sendRequest({
        method: "POST",
        url: api_prefix + "/groups/" + groupId,
        data: formData,
      });
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo guardar la imagen del grupo: " + error,
      });
    }
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
