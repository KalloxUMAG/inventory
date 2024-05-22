<template>
  <PageTitle title="Usuarios" icon="person" />
  <q-card class="no-shadow bg-transparent">
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md space-between">
        Lista de Usuarios
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
            to="/users/new_user"
            icon="person_add"
            label="Agregar"
            flat
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        row-key="id"
        :columns="usersColumns"
        :rows="users"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        @row-click="rowClicker"
        flat
        bordered
        wrap-cells
        :filter="filter"
        class="card-style"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              :class="['text-italic', 'table-header', col.additionalClass]"
            >
              {{ col.label }}
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body-cell="props">
          <q-td :props="props">
            {{ props.value }}
          </q-td>
        </template>
        <template v-slot:body-cell-img="props">
          <q-td>
            <q-avatar square text-color="white" size="56px">
              <q-img
                v-if="props.value != null"
                :src="api_prefix.slice(0, -4) + props.value"
                spinner-color="white"
              />
              <q-img v-else src="~assets/no-image.png" spinner-color="white" />
            </q-avatar>
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance";

import PageTitle from "src/components/commons/PageTitle.vue";
import { usersColumns } from "src/constants/columns";

const router = useRouter();

const users = ref([]);
const filter = ref("");

const api_prefix = process.env.API_URL;
const img_url = api_prefix + "/users/images/";
const detail_query = "/users/";

const getUsers = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/users",
    });
    users.value = response.data;
    users.value.forEach(async (user) => {
      user.img = await getUserImage(user.id);
    });
  } catch (error) {}
};

const getUserImage = async (user_id) => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: img_url + user_id,
    });
    return response.data[0].path;
  } catch (error) {
    return null;
  }
};

const rowClicker = (e, row) => {
  const item = row.id;
  router.push(detail_query + item);
};

onMounted(() => {
  getUsers();
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
.image-visor {
  border: none !important;
  padding: 0;
}

.width-300 {
  width: 300px;
}
</style>
