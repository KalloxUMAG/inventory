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

    <q-card class="my-card row q-pa-md gap-lg" flat bordered>
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

const route = useRoute()
const router = useRouter()
const id = computed(() => route.params.id)
const api_prefix = process.env.API_URL
const query_groups = `${api_prefix}/groups/${id.value}`
const img_url = `${api_prefix}/groups/image/`
const $q = useQuasar()

const group = ref(null)
const images = ref(null)

// Functions
function editGroup() {
  router.push(`/groups/edit/${id.value}`)
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

async function getImages() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: img_url + id.value,
    })
    images.value = response.data
    console.log(api_prefix + images.value[0].path)
  }
  catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  getGroup()
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
</style>
