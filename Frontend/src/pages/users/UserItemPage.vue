<template>
  <div v-if="user != null" class="row justify-center">
    <PageTitle :title="user.fullname" icon="person">
      <div>
        <q-btn outline color="secondary" label="Editar" disable @click="editUser" />
        <q-btn v-if="user.disable"
          class="q-ml-sm"
          color="positive"
          label="Reactivar"
          @click="activateUser"
        />
        <q-btn v-else
          class="q-ml-sm"
          color="negative"
          label="Desactivar"
          @click="deleteUser"
        />
      </div>
    </PageTitle>

    <q-card class="my-card row q-pa-md q-mb-lg gap-lg" flat bordered>
      <div class="col-12 col-sm-3 container image-visor">
        <q-img
          v-if="images != null"
          class="rounded-borders"
          :src="api_prefix.slice(0, -4) + images[0].path"
          spinner-color="white"
          style="height: 100%"
          fit="contain"
        />
        <div v-else class="rounded-borders no-image">
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

    <q-card class="col-12" flat bordered>
      <q-card-section>
        <div class="text-h5 text-weight-bold q-pl-md space-between">
          Grupos
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section>
        <div class="q-pa-md">
          <q-list>
            <q-item v-for="group in user.group_roles" :key="group.group_id">
              <q-item-section>
                <q-item-label>
                  <q-badge color="primary" label="Grupo" />
                  {{ group.group_name }} ({{ group.role_name }})
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { sendRequest } from 'src/services/axios/instance.js'
import { useQuasar } from 'quasar'
import { reactivateUser } from 'src/services'

// Components
import DeleteDialog from 'src/components/item-page/DeleteDialog.vue'
import InfoSection from 'src/components/item-page/InfoSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

// Constants
const route = useRoute()
const router = useRouter()
const $q = useQuasar()
const id = computed(() => route.params.id)
const user = ref(null)
const images = ref(null)
const api_prefix = process.env.API_URL
const query_users = `${api_prefix}/users/${id.value}`
const img_url = `${api_prefix}/users/images/`

// Methods
async function getUser() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: query_users,
    })
    user.value = response.data
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
    images.value = response.data
  }
  catch (error) {
    console.log(error)
  }
}

function editUser() {
  router.push(`/users/edit/${id.value}`)
}

function deleteUser() {
  $q.dialog({
    component: DeleteDialog,
    componentProps: {
      id: id.value,
      title: `Usuario: ${user.value.fullname}`,
      type: 'users',
    },
  })
    .onOk(async(data) => {
      await getUser()
    })
    .onCancel(() => {})
}

async function activateUser() {
  await reactivateUser(id.value)
  await getUser()
}

onMounted(() => {
  getUser()
})
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
