<template>
  <PageTitle title="Insumos" icon="science"/>
  <q-card class="no-shadow bg-transparent" >
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md space-between">
        Lista de insumos
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
            to="/supplies/new_supply"
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
        :columns="suppliesColumns"
        :rows="supplies"
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
            <q-th auto-width>Lotes</q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props" class="item-row">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              @click="rowClicker(props.row)"
            >
              {{ col.value }}
            </q-td>
            <q-td auto-width>
              <q-btn size="sm" align="between" color="accent" flat @click="props.expand = !props.expand" :icon-right="props.expand ? 'expand_less':'expand_more'"/>
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td class="subtable" colspan="100%">
              <q-table
                :rows="props.row.lots"
                :columns="lotsColumns"
                row-key="id"
                flat
                no-wrap
                hide-bottom
                card-class="bg-grey-1 text-grey-8"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { sendRequest } from "src/axios/instance";
import { suppliesColumns, lotsColumns } from "../constants/columns.js";
import { useRouter } from "vue-router";

import PageTitle from "src/components/commons/PageTitle.vue";

const supplies = ref([]);
const api_prefix = process.env.API_URL;

const router = useRouter();
const filter = ref("");
const detail_query = "/supplies/";

const getSupplies = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/supplies",
    });
    supplies.value = response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock;
      supply.critical = supply.stock <= supply.critical_stock ? true : false;
      return supply;
    });
  } catch (error) {}
};

const rowClicker = (row) => {
  const item = row.id;
  router.push(detail_query + item);
};

onMounted(() => {
  getSupplies();
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
 .item-row{
  cursor: pointer;
 }
 .subtable{
  padding: 0;
 }
</style>