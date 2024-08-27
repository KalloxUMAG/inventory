<template>
  <q-card class="no-shadow q-pa-xs card-style" bordered>
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md row">
        <div class="col-8">
          <span class="text-red text-uppercase text-bold">¡Importante!</span> {{ title }}
        </div>
        <div class="col-4">
          <q-btn flat icon-right="arrow_forward" label="Ver todos" :to="detail_query" class="text-gray-8 non-selectable no-outline float-right" />
        </div>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section class="q-pa-none q-mt-sm">
      <q-table
        :grid="$q.screen.xs"
        :row-key="row_key"
        :columns="columns"
        :rows="rows"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        hide-bottom
        flat
        bordered
        no-wrap
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
