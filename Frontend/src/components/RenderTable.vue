<template>
  <q-table class="q-mt-md" :title="title" :columns="columns" :rows="rows" no-data-label="No hay registros para mostrar" />
</template>

<script>
export default {
  props: {
    columns: Array,
    title: String,
    rows: Array,
  },

  setup() {
    return {
    };
  },
};
</script>
