<template>
  <q-page padding>
    <h3>Equipamiento</h3>
    <RenderTable :columns="columns" :rows="this.equipments" title="Equipamiento" />
    <pre>{{ this.equipments }}</pre>
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
    name: "location",
    align: "left",
    label: "Ubicacion",
    field: "location",
    sortable: true,
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
    name: "stage",
    align: "left",
    label: "Proyecto",
    field: "stage",
    sortable: false,
  },
  {
    name: "maintenance",
    align: "left",
    label: "Mantencion",
    field: "maintenance",
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
