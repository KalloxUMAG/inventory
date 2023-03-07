<template>
  <q-table class="q-mt-md" :title="title" row-key="name" :columns="columns" :rows="rows" no-data-label="No hay registros para mostrar" selection="single" v-model:selected="selected">
    <template v-slot:top>
      <q-btn color="positive" label="Agregar" />
      <q-btn class="q-ml-sm" color="warning" label="Modificar selección" />
      <q-btn class="q-ml-sm" color="negative" label="Eliminar selección" />
      <q-space />
      <q-input outlined dense debounce="300" placeholder="Buscar" color="primary">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template #body-cell-contacts="props">
      <q-td :props="props">
        <q-btn dense label="Ver contactos" color="blue" field="edit" ></q-btn>
      </q-td>
    </template>
    <template #body-cell-edit="props">
      <q-td :props="props">
        <q-btn dense flat round color="blue" field="edit" icon="edit" ></q-btn>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { ref } from 'vue';

const addlabel = "Agregar"
export default {
  props: {
    columns: Array,
    title: String,
    rows: Array,
  },

  setup() {
    return {
      addlabel,
      selected: ref([])
    };
  },
};
</script>
