<template>
  <q-page padding>
    <RenderTable
      :columns="columns"
      :rows="lots"
      title="Insumos"
      detail_query="/supplies/"
      row_key="id"
    />
    {{ lots }}
  </q-page>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const columns = [
  {
    name: "supply_name",
    align: "left",
    label: "Nombre",
    field: "supply_name",
    sortable: false,
  },
  {
    name: "supply_code",
    align: "left",
    label: "Codigo",
    field: "supply_code",
    sortable: false,
  },
  {
    name: "number",
    align: "left",
    label: "Lote",
    field: "number",
    sortable: false,
  },
  {
    name: "due_date",
    align: "left",
    label: "Fecha de vencimiento",
    field: "due_date",
    sortable: true,
  },
  {
    name: "location",
    align: "left",
    label: "Localizacion",
    field: "location",
    sortable: true,
  },
  {
    name: "sub_location",
    align: "left",
    label: "Sub-localizacion",
    field: "sub_location",
    sortable: true,
  },
  {
    name: "stock",
    align: "left",
    label: "Stock",
    field: "stock",
    sortable: false,
  },
  {
    name: "supplier_name",
    align: "left",
    label: "Proveedor",
    field: "supplier_name",
    sortable: false,
  },
  {
    name: "observations",
    align: "left",
    label: "Observacion",
    field: "observations",
    sortable: false,
  },
  {
    name: "details",
    align: "center",
    label: "Detalles",
    field: "details",
    sortable: false,
  },
];

const lots = ref([]);

const getLots = () => {
  axios
    .get("http://localhost:8000/api/lots")
    .then((response) => (lots.value = response.data));
};

onMounted(() => {
  getLots();
});
</script>
