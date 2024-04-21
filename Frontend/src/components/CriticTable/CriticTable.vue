<template>
  <q-table
    :row-key="row_key"
    :columns="columns"
    :rows="rows"
    no-data-label="No hay registros para mostrar"
    rows-per-page-label="Registros por pagina"
    @row-click="rowClicker"
    hide-bottom
    flat
    bordered
    no-wrap
    class="card-style"
  >
    <template v-slot:body-cell="props">
      <q-td
        :props="props"
      >
        {{ props.value }}
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { ref } from "vue";
export default {
  props: {
    columns: Array,
    rows: Array,
    detail_query: String,
    row_key: String,
  },
  methods: {
    rowClicker(e, row) {
      const item = row.id;
      this.$router.push(this.detail_query + item);
    },
  },
};
</script>

<style scoped>
 .card-style{
  border-radius: 12px;
 }
</style>
