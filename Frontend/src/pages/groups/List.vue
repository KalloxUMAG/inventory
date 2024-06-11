<template>
  <PageTitle title="Grupos" icon="groups" />
  <q-card class="no-shadow bg-transparent">
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md space-between">
        Lista de Grupos
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
            to="/groups/new_group"
            icon="add"
            label="Agregar"
            flat
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        row-key="id"
        :columns="groupsColumns"
        :rows="groups"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        flat
        bordered
        wrap-cells
        :filter="filter"
        class="card-style"
        @row-click="rowClicker"
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
          <q-td
            :props="props"
          >
            {{ props.value }}
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'
import { sendRequest } from 'src/services/axios/instance'

import PageTitle from 'src/components/commons/PageTitle.vue'
import { groupsColumns } from 'src/constants/columns'

const router = useRouter()

const groups = ref([])
const filter = ref('')

const api_prefix = process.env.API_URL
const detail_query = '/groups/'

async function getGroups() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/groups`,
    })
    groups.value = response.data
    groups.value.forEach((group) => {
      group.other_names = group.other_names.join('; ')
    })
  }
  catch (error) {}
}

function rowClicker(e, row) {
  const item = row.id
  router.push(detail_query + item)
}

onMounted(() => {
  getGroups()
})
</script>

<style scoped>
.card-style {
  border-radius: 12px;
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
