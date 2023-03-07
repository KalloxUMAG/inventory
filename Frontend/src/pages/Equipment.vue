<template>
  <q-page padding>
    <h1>Equipamiento</h1>
    <RenderTable :columns="columns" :rows="rows" title="Equipamiento" />
    <pre>{{ this.equipments }}</pre>
  </q-page>
</template>

<script>
import RenderTable from "src/components/RenderTable.vue";
import axios from 'axios'

const columns = [
  {
    name: "id",
    label: "Numero",
    align: "left",
    field: "id",
    sortable: true,
  },
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "stage",
    align: "left",
    label: "Etapa",
    field: "stage",
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
    name: "date2",
    align: "left",
    label: "Fecha",
    field: "date2",
    sortable: false,
  },
];

  const rows = [
    {
      id: 0,
      name: "Gran equipo 1",
      stage: "Proyecto Terra, Junio",
      serial_number: "7748823DA",
      location: "UMAG - Ingenieria - Magister",
      invoice_number: "878477",
      umag_inventory_code: 8837875,
    },
  ]

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
      rows
    };
  },
};
</script>
