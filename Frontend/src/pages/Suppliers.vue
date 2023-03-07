<template>
  <q-page padding>
      <h1>Proveedores</h1>
      <RenderTable :columns="columns" :rows="rows" title="Proveedores" />
    </q-page>
</template>

<script>
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
      label: "Nombre",
      align: "left",
      field: "name",
      sortable: true,
    },
    {
      name: "rut",
      label: "Rut",
      align: "left",
      field: "rut",
      sortable: true,
    },
    {
      name: "city_address",
      label: "Dirección",
      align: "left",
      field: "city_address",
      sortable: true,
    },
    {
      name: "contacts",
      label: "Contactos",
      align: "left",
      field: "contacts",
      sortable: false,
    },
    {
      name: "edit",
      label: "Editar",
      align: "left",
      field: "edit",
      sortable: false,
    },
  ]

  const rows = [
    {
      id: 0,
      name: "Amazon",
      rut: "1433342-6",
      city_address: "Santiago, Salvador allende 04211",
      contacts: "test"
    },
    {
      id: 1,
      name: "Amazon 2",
      rut: "1433342-6",
      city_address: "Santiago, Salvador allende 04333",
      contacts: "test"
    },
    {
      id: 2,
      name: "Apple",
      rut: "1433342-6",
      city_address: "Iquique, Arauco 4882",
      contacts: "test"
    },
    {
      id: 3,
      name: "Lider",
      rut: "1433342-6",
      city_address: "Santiago, San festin 281",
      contacts: "test"
    },
  ]

  import RenderTable from "src/components/RenderTable.vue";
  export default {
    components: { RenderTable },
    setup(){
      return{
        columns,
        rows
      }
    }
  }
</script>
