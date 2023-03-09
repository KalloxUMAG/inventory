<template>
  <q-table class="q-mt-md" :title="title" row-key="id" :columns="columns" :rows="rows" no-data-label="No hay registros para mostrar">
    <template v-slot:top>
      <q-btn color="positive" label="Agregar" />
      <q-space />
      <q-input outlined dense debounce="300" placeholder="Buscar" color="primary">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template #body-cell-details="props">
      <q-td :props="props">
        <q-btn dense flat label="ver detalles" color="blue" field="details" icon="info" @click.prevent="load_details(props.row)" />
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
  methods: {
    load_details(item){
      this.$router.push('/equipments/'+item.id)
    }
  },
  setup() {
    return {
      addlabel,
      selected: ref([]),
    };
  },
};
</script>
