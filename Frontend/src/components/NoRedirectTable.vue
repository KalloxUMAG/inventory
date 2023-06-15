<template>
  <q-table
    :title="title"
    row-key="id"
    :columns="columns"
    :rows="rows"
    no-data-label="No hay registros para mostrar"
    :filter="filter"
  >
    <template v-slot:top>
      <h1 class="text-h5">{{ title }}</h1>
      <q-space />
      <q-btn
        color="positive"
        label="Agregar"
        class="q-mr-sm"
        @click="addFunction"
      />
      <q-input
        outlined
        dense
        debounce="300"
        placeholder="Buscar"
        color="primary"
        v-model="filter"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template v-slot:body-cell-action="props">
      <q-td :props="props">
        <q-btn flat dense icon="delete" color="negative" @click="deleteFunction(props.row)"/>
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
    addFunction: Function,
    deleteFunction: Function,
  },
  methods: {
    load_details(item) {
      this.$router.push("/equipments/" + item.id);
    },
  },
  setup() {
    const filter = ref("");
    return {
      addlabel,
      selected: ref([]),
      filter,
    };
  },
};
</script>
