<template>
  <q-table
    :title="title"
    :row-key="row_key"
    :columns="columns"
    :rows="rows"
    no-data-label="No hay registros para mostrar"
    rows-per-page-label="Registros por pagina"
    :filter="filter"
    v-model:pagination="pagination"
    @row-click="rowClicker"
    card-class="text-grey-8 bg-white"
    table-header-class="text-black"
  >
    <template v-slot:top>
      <h1 class="text-h5">{{ title }}</h1>
      <q-space />
      <q-btn
        v-if="addTo != null"
        class="add-btn q-mr-sm"
        :to="addTo"
        icon="add"
        rounded
      />
      <q-input
        outlined
        dense
        debounce="300"
        placeholder="Buscar"
        v-model="filter"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template v-slot:body-cell="props">
      <q-td
        :props="props"
        :class="
          (props.row.critical && 'bg-amber-2') ||
          ((!props.row.stage_id || !props.row.invoice_id) && 'bg-red-3')
        "
      >
        {{ props.value }}
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { ref } from "vue";
const addlabel = "Agregar";
export default {
  props: {
    columns: Array,
    title: String,
    rows: Array,
    detail_query: String,
    row_key: String,
    addTo: String,
  },
  methods: {
    rowClicker(e, row) {
      const item = row.id;
      this.$router.push(this.detail_query + item);
    },
  },
  setup() {
    const filter = ref("");
    const pagination = ref({
      rowsPerPage: 10,
    });
    return {
      addlabel,
      selected: ref([]),
      filter,
      pagination,
    };
  },
};
</script>

<style lang="scss" scoped>
.add-btn {
  background-color: #5390eb;
  color: #fefefe;
}
</style>
