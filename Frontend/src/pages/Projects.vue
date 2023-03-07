<template>
  <q-page padding>
      <h1>Proyectos</h1>
      <RenderTable :columns="columns" :rows="[]" title="Proyectos" />
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
    label: "Proyecto",
    align: "left",
    field: "name",
    sortable: true,
  },
  {
    name: "start",
    label: "Inicio",
    align: "left",
    field: "start",
    sortable: true,
  },
  {
    name: "end",
    label: "Termino",
    align: "left",
    field: "end",
    sortable: true,
  },
  {
    name: "stage",
    label: "Etapa actual",
    align: "left",
    field: "stages",
    sortable: false,
  },
  {
    name: "equipments",
    label: "Equipos",
    align: "left",
    field: "equipments",
    sortable: false,
  },
]
  import RenderTable from "src/components/RenderTable.vue";
  export default {
    components: { RenderTable },
    setup(){
      return{
        columns
      }
    }
  }
</script>
