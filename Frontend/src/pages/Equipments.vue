<template>
  <q-page padding>
    <RenderTable :columns="columns" :rows="this.equipments" title="Equipamiento" detail_query="/equipments/" row_key="name"/>
  </q-page>
</template>

<script>
import RenderTable from "src/components/RenderTable.vue";
import axios from 'axios'

const columns = [
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "serial_number",
    align: "left",
    label: "Nro. serie",
    field: "serial_number",
    sortable: false,
  },
  {
    name: "invoice_number",
    align: "left",
    label: "Factura",
    field: "invoice_number",
    sortable: false,
  },
  {
    name: "supplier_name",
    align: "left",
    label: "Proveedor",
    field: "supplier_name",
    sortable: true,
  },
  {
    name: "umag_inventory_code",
    align: "left",
    label: "Inventariado",
    field: "umag_inventory_code",
    sortable: true,
  },
  {
    name: "last_preventive_maintenance",
    align: "left",
    label: "Mantención",
    field: "last_preventive_maintenance",
    sortable: true,
  },
  {
    name: "reception_date",
    align: "left",
    label: "Fecha",
    field: "reception_date",
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

export default {
  components: { RenderTable },
  data(){
    return{
      equipments: []
    }
  },
  methods:{
    getEquipments(){
      axios.get("http://localhost:8000/api/equipments").then(
        response => (
          this.equipments = response.data
        )
      )
    }
  },
  mounted(){
    this.getEquipments();
  },
  setup() {
    return {
      columns,
    };
  },
};
</script>
