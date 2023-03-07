<template>
  <q-page padding>
      <h1>Ubicaciones</h1>
      <RenderTable :columns="columns" :rows="[]" title="Ubicaciones" />
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
    name: "building",
    label: "Edificio",
    align: "left",
    field: "building",
    sortable: true,
  },
  {
    name: "unit",
    label: "Unidad",
    align: "left",
    field: "unit",
    sortable: true,
  },
  {
    name: "room",
    label: "Sala",
    align: "left",
    field: "room",
    sortable: true,
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
