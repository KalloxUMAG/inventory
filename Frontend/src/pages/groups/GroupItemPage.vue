<template>
  <div v-if="group != null" class="row justify-center">
    <PageTitle :title="group.name" icon="group">
      <div>
        <q-btn
          outline
          color="secondary"
          label="Editar"
          @click="editGroup"
        />
        <q-btn
          class="q-ml-sm"
          color="negative"
          label="Eliminar"
          @click="deleteGroup"
        />
      </div>
    </PageTitle>

    <q-card class="my-card row q-pa-md gap-lg q-mb-lg" flat bordered>
      <div class="col-12 col-sm-3 container image-visor">
        <q-img
          v-if="images != null"
          class="rounded-borders"
          :src="api_prefix.slice(0, -4) + images[0].path"
          spinner-color="white"
          style="height: 100%;"
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
              label: 'Nombre',
              value: group.name,
            },
            {
              label: 'Descripción',
              value: group.description,
            },
            {
              label: 'Otros nombres',
              value: group.other_names,
              type: 'list',
            },
          ]"
        />
      </div>
    </q-card>

    <q-card class="my-card row q-pa-md gap-lg no-shadow" flat bordered="">
      <q-card-section class="q-pl-none col-12">
        <div class="text-subtitle1 q-pl-md space-between">
          Lista de Usuarios
          <div class="actions-buttons">
            <q-input
              v-model="filter"
              outlined
              bg-color="white"
              dense
              debounce="300"
              placeholder="Buscar"
            >
              <template #append>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-btn
              class="add-btn q-mr-sm"
              to="/users/new_user"
              icon="person_add"
              label="Agregar"
              flat
            />
          </div>
        </div>
      </q-card-section>
      <q-card-section class="q-pa-none col-12">
        <q-table
          :grid="$q.screen.xs"
          row-key="user_id"
          :columns="groupUsersColumns"
          :rows="users"
          no-data-label="No hay registros para mostrar"
          rows-per-page-label="Registros por pagina"
          flat
          bordered
          wrap-cells
          :filter="filter"
          class="card-style"
        >
          <template #header="props">
            <q-tr :props="props">
              <q-th
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
                class="text-italic table-header" :class="[col.additionalClass]"
              >
                {{ col.label }}
              </q-th>
            </q-tr>
          </template>
          <template #body-cell="props">
            <q-td :props="props">
              {{ props.value }}
            </q-td>
          </template>
          <template #body-cell-img="props">
            <q-td>
              <q-avatar square text-color="white" size="56px">
                <q-img
                  v-if="props.value != null"
                  :src="api_prefix.slice(0, -4) + props.value"
                  spinner-color="white"
                />
                <q-img v-else src="/images/no_img.png" spinner-color="white" />
              </q-avatar>
            </q-td>
          </template>
          <template #body-cell-status="props">
            <q-td>
              <q-chip v-if="!props.row.disable" color="teal" text-color="white" icon="check">
                Activo
                <q-tooltip>Los usuarios activos pueden iniciar sesión. Para desactivarlos contacta con un administrador.</q-tooltip>
              </q-chip>
              <q-chip v-if="props.row.disable" color="red" text-color="white" icon="block">
                Desactivado
                <q-tooltip>Los usuarios desactivados no pueden iniciar sesión. Para volver a activarlo contacta con un administrador.</q-tooltip>
              </q-chip>
            </q-td>
          </template>
          <template #body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                v-if="props.row.user_id != null"
                flat
                dense
                icon="delete"
                color="negative"
                @click="removeUser(props.row)"
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { sendRequest } from 'src/services/axios/instance.js'
import { useQuasar } from 'quasar'

// Components
import DeleteDialog from 'src/components/item-page/DeleteDialog.vue'
import InfoSection from 'src/components/item-page/InfoSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

import { groupUsersColumns } from 'src/constants/columns'
import { deleteUserGroupRole, getUsersFromGroup } from 'src/services'

const route = useRoute()
const router = useRouter()
const id = computed(() => route.params.id)
const api_prefix = process.env.API_URL
const query_groups = `${api_prefix}/groups/${id.value}`
const img_url = `${api_prefix}/groups/image/`
const user_img_url = `${api_prefix}/users/images/`
const $q = useQuasar()

const group = ref(null)
const images = ref(null)

const users = ref([])

const filter = ref('')

// Functions
function editGroup() {
  router.push(`/groups/edit/${id.value}`)
}

function removeUser(user) {
  $q.dialog({
    title: 'Eliminar usuario del grupo',
    message: 'Estás seguro de que deseas eliminar este usuario del grupo?',
    ok: {
      color: 'negative',
      label: 'Aceptar y eliminar',
    },
    cancel: {
      color: 'warning',
      label: 'Cancelar y mantener',
    },
  })
    .onOk(async () => {
      const user_id = user.user_id
      await deleteUserGroupRole(user_id, id.value)
      await getGroupUsers()
    })
}

function deleteGroup() {
  $q.dialog({
    component: DeleteDialog,
    componentProps: {
      id: id.value,
      title: `grupo: ${group.value.name}`,
      type: 'groups',
    },
  })
    .onOk((data) => {
      router.push('/groups')
    })
    .onCancel(() => {})
}

async function getGroup() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: query_groups,
    })
    group.value = response.data
    getImages()
  }
  catch (error) {
    console.log(error)
  }
}

async function getGroupUsers() {
  users.value = await getUsersFromGroup(id.value)
  users.value.forEach(async (user) => {
    user.img = await getUserImage(user.user_id)
  })
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

async function getUserImage(user_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: user_img_url + user_id,
    })
    console.log(response.data[0].path)
    return response.data[0].path
  }
  catch (error) {
    return null
  }
}

onMounted(() => {
  getGroup()
  getGroupUsers()
})
</script>

<style scoped>
.container {
  border: 1px solid #d1d1d1 !important;
  border-radius: 12px !important;
  padding: 8px;
  overflow: visible;
}

.gap-lg{
  gap: 24px;
}

.image-visor{
  border: none !important;
  height: 250px;
  widows: 250px;
  padding: 0;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}

.no-image{
    align-items: center;
    background-color: #eef3f7;
    color: #6c757d;
    display: flex;
    height: 100%;
    justify-content: center;
    font-size: 24px;
}

.space-between {
  display: flex;
  justify-content: space-between;
}

.actions-buttons {
  display: inline-flex;
  gap: 10px;

  .add-btn {
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
}
</style>
