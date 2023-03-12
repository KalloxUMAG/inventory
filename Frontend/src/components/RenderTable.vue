<template>
  <q-table :title="title" :row-key="row_key" :columns="columns" :rows="rows" no-data-label="No hay registros para mostrar" :filter="filter">
    <template v-slot:top>
      <h1 class="text-h5">{{ title }}</h1>
      <q-space/>
      <q-btn color="positive" label="Agregar" class="q-mr-sm" to="/equipments/new_equipment"/>
      <q-input outlined dense debounce="300" placeholder="Buscar" color="primary" v-model="filter">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template #body-cell-details="props">
      <q-td :props="props">
        <q-btn dense flat label="ver detalles" class="bg-blue" color="white" field="details" icon="info" @click.prevent="load_details(props.row)" />
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
    detail_query: String,
    row_key: String,
  },
  methods: {
    load_details(item){
      this.$router.push(this.detail_query+item.id)
    }
  },
  setup() {
    const filter = ref('')
    return {
      addlabel,
      selected: ref([]),
      filter,
    };
  },
};
</script>
