<template>
  <q-card class="no-shadow bg-transparent" >
        <q-card-section class="q-pl-none col-12">
          <div class="text-subtitle1 q-pl-md space-between">
            Lista de equipamientos
            <div class="actions-buttons">
              <q-input
                outlined
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
                to="/equipments/new_equipment"
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
            :columns="equipmentsColumns"
            :rows="equipments"
            no-data-label="No hay registros para mostrar"
            rows-per-page-label="Registros por pagina"
            @row-click="rowClicker"
            flat
            bordered
            no-wrap
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
              <q-td
                :props="props"
              >
                {{ props.value }}
              </q-td>
            </template>
            <template v-slot:body-cell-state="props">
              <q-td :props="props" auto-width>
                <!-- Mostrar icono si state es false, de lo contrario mostrar texto normal -->
                <div class="state-col">
                  <q-icon v-if="!props.row.state" name="error" color="red">
                    <q-tooltip class="bg-negative" :offset="[10, 10]">
                      Realizar mantenimiento
                    </q-tooltip>
                  </q-icon>
                </div>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import { onMounted, ref } from "vue";
import { equipmentsColumns } from "../constants/columns.js";

import { useRouter } from "vue-router";
import { sendRequest } from "src/axios/instance";

const router = useRouter();

const equipments = ref([]);
const filter = ref("");

const api_prefix = process.env.API_URL;
const detail_query = "/equipments/";

const getEquipments = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/equipments",
    });
    equipments.value = response.data;
  } catch (error) {
  }
};

const rowClicker = (e, row) => {
  const item = row.id;
  router.push(detail_query + item);
};

onMounted(() => {
  getEquipments();
});

</script>

<style scoped>
 .card-style{
  border-radius: 12px;
 }
 .space-between{
  display: flex;
  justify-content: space-between;
 }
 .actions-buttons{
  display: inline-flex;
  gap: 10px;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
 }
</style>
