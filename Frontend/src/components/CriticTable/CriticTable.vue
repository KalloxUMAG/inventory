<template>
  <q-card class="no-shadow bg-transparent">
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md">
        <span class="text-red text-uppercase text-bold">¡Importante!</span> {{ title }}
        <q-btn flat icon-right="arrow_forward" label="Ver todos" to="/supplies/" class="text-gray-8 non-selectable no-outline float-right" />
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        :row-key="row_key"
        :columns="columns"
        :rows="rows"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        hide-bottom
        flat
        bordered
        no-wrap
        class="card-style"
        @row-click="rowClicker"
      >
        <template #body-cell="props">
          <q-td
            :props="props"
          >
            {{ props.value }}
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: {
    title: String,
    columns: Array,
    rows: Array,
    detail_query: String,
    row_key: String,
  },
  methods: {
    rowClicker(e, row) {
      const item = row.id
      this.$router.push(this.detail_query + item)
    },
  },
}
</script>

<style scoped>
 .card-style{
  border-radius: 12px;
 }
</style>
