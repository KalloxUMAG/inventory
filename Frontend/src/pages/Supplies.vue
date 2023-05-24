<template>
  <q-page padding>
    <div>
      <RenderTable
        :columns="suppliesColumns"
        :rows="supplies"
        title="Insumos"
        detail_query="/supplies/"
        row_key="id"
        addTo="/supplies/new_supply"
      />
    </div>
    <div class="q-mt-xl">
      <RenderTable
        :columns="lotsColumns"
        :rows="lots"
        title="Lotes"
        detail_query="/supplies/lot/"
        row_key="id"
        addTo="/supplies/new_lot"
      />
    </div>
  </q-page>
</template>

<script setup>
import RenderTable from "src/components/RenderTable.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const lotsColumns = [
  {
    name: "supply_name",
    align: "left",
    label: "Insumo",
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
  }
];

const suppliesColumns = [
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "code",
    align: "left",
    label: "Codigo",
    field: "code",
    sortable: false,
  },
  {
    name: "cost",
    align: "left",
    label: "Costo",
    field: "cost",
    sortable: false,
  },
  {
    name: "supplies_brand_name",
    align: "left",
    label: "Marca",
    field: "supplies_brand_name",
    sortable: true,
  },
  {
    name: "supplies_type_name",
    align: "left",
    label: "Tipo de insumo",
    field: "supplies_type_name",
    sortable: true,
  },
  {
    name: "supplier_name",
    align: "left",
    label: "Proveedor",
    field: "supplier_name",
    sortable: true,
  },
];

const lots = ref([]);
const supplies = ref([]);

const getLots = () => {
  axios
    .get("http://localhost:8000/api/lots")
    .then((response) => (lots.value = response.data));
};

const getSupplies = () => {
  axios
    .get("http://localhost:8000/api/supplies")
    .then((response) => (supplies.value = response.data));
};

onMounted(() => {
  getLots();
  getSupplies();
});
</script>
