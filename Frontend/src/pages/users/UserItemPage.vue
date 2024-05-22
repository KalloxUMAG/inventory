<template>
  <div v-if="user != null" class="row justify-center">
    <PageTitle :title="user.fullname" icon="person">
      <div>
        <q-btn outline color="secondary" label="Editar" @click="editUser" disable/>
        <q-btn
          class="q-ml-sm"
          color="negative"
          label="Eliminar"
          @click="deleteUser"
          disable
        />
      </div>
    </PageTitle>

    <q-card class="my-card row q-pa-md gap-lg" flat bordered>
      <div class="col-12 col-sm-3 container image-visor">
        <q-img
          v-if="images != null"
          class="rounded-borders"
          :src="api_prefix.slice(0, -4) + images[0].path"
          spinner-color="white"
          style="height: 100%"
          fit="contain"
        />
        <div class="rounded-borders no-image" v-else>
          No hay imagen disponible
        </div>
      </div>

      <div class="col container">
        <InfoSection
          title="Información general"
          :fields="[
            {
              label: 'Nombre completo',
              value: user.fullname,
            },
            {
              label: 'Correo',
              value: user.email,
            },
          ]"
        />
      </div>
    </q-card>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance.js";
import { useQuasar } from "quasar";

// Components
import DeleteDialog from "src/components/item-page/DeleteDialog.vue";
import InfoSection from "src/components/item-page/InfoSection.vue";
import PageTitle from "src/components/commons/PageTitle.vue";

// Constants
const route = useRoute();
const router = useRouter();
const $q = useQuasar();
const id = computed(() => route.params.id);
const user = ref(null);
const images = ref(null);
const api_prefix = process.env.API_URL;
const query_users = api_prefix + "/users/" + id.value;
const img_url = api_prefix + "/users/images/";

// Methods
const getUser = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: query_users,
    });
    user.value = response.data;
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
    images.value = response.data;
  } catch (error) {
    console.log(error);
  }
};

const editUser = () => {
  router.push("/users/edit/" + id.value);
};

const deleteUser = () => {
  $q.dialog({
    component: DeleteDialog,
    componentProps: {
      id: id.value,
      title: "Usuario: " + user.value.fullname,
      type: "users",
    },
  })
    .onOk((data) => {
      router.push("/users");
    })
    .onCancel(() => {});
};

onMounted(() => {
  getUser();
});
</script>

<style scoped>
.container {
  border: 1px solid #d1d1d1 !important;
  border-radius: 12px !important;
  padding: 8px;
  overflow: visible;
}

.gap-lg {
  gap: 24px;
}

.image-visor {
  background-color: #f5f5f5;
  border: none !important;
  height: 250px;
  widows: 250px;
  padding: 0;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}

.no-image {
  align-items: center;
  background-color: #eef3f7;
  color: #6c757d;
  display: flex;
  height: 100%;
  justify-content: center;
  font-size: 24px;
}
</style>
