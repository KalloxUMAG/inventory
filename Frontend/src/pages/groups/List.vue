<template>
  <PageTitle title="Grupos" icon="groups" />
  <q-card class="no-shadow bg-transparent">
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md space-between">
        Lista de Grupos
        <div class="actions-buttons">
          <q-input
            outlined
            bg-color="white"
            dense
            debounce="300"
            placeholder="Buscar"
            v-model="filter"
          >
            <template v-slot:append>
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
            @row-click="rowClicker"
            flat
            bordered
            no-wrap
            :filter="filter"
            class="card-style"
        />
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance";

import PageTitle from "src/components/commons/PageTitle.vue";

const router = useRouter();

const groups = ref([]);
const filter = ref("");

const api_prefix = process.env.API_URL;
const detail_query = "/groups/";

const getGroups = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/groups",
    });
    groups.value = response.data;
  } catch (error) {}
};

const rowClicker = (e, row) => {
  const item = row.id;
  router.push(detail_query + item);
};

onMounted(() => {
  getGroups();
});
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
