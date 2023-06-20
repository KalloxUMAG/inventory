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
    <template v-slot:body-cell-actions="props">
      <q-td :props="props">
        <q-btn flat dense icon="edit" color="warning" @click="editFunction(props.row)"/>
        <q-btn flat dense icon="delete" color="negative" @click="deleteFunction(props.row)"/>
      </q-td>
    </template>
    <template v-slot:body-cell-state="props">
      <q-td :props="props">
        <q-btn v-if="props.row.state == true" flat dense icon="done_all" color="positive"/>
        <q-btn v-if="props.row.state == false" flat dense icon="close" color="negative"/>
        <q-btn v-if="props.row.state == null" flat dense icon="play_arrow" color="warning"/>
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
    editFunction: Function,
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
