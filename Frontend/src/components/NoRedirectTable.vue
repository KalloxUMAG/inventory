<template>
  <q-table
    :grid="$q.screen.xs"
    :title="title"
    row-key="id"
    :columns="columns"
    :rows="rows"
    no-data-label="No hay registros para mostrar"
    rows-per-page-label="Registros por pagina"
    :filter="filter"
  >
    <template #top>
      <h1 class="text-h5">
        {{ title }}
      </h1>
      <q-space />
      <q-btn
        color="positive"
        label="Agregar"
        class="q-mr-sm"
        @click="addFunction"
      />
      <q-input
        v-model="filter"
        outlined
        dense
        debounce="300"
        placeholder="Buscar"
        color="primary"
      >
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template #body-cell-action="props">
      <q-td :props="props">
        <q-btn
          flat
          dense
          icon="delete"
          color="negative"
          @click="deleteFunction(props.row)"
        />
      </q-td>
    </template>
    <template #body-cell-actions="props">
      <q-td :props="props">
        <q-btn
          flat
          dense
          icon="edit"
          color="warning"
          @click="editFunction(props.row)"
        />
        <q-btn
          v-if="props.row.id != null"
          flat
          dense
          icon="delete"
          color="negative"
          @click="deleteFunction(props.row)"
        />
      </q-td>
    </template>
    <template #body-cell-state="props">
      <q-td :props="props">
        <q-icon
          v-if="props.row.state == true"
          size="md"
          name="done_all"
          color="positive"
        >
          <q-tooltip>Realizado</q-tooltip>
        </q-icon>
        <q-icon
          v-if="props.row.state == false"
          size="md"
          name="close"
          color="negative"
        >
          <q-tooltip>No realizado</q-tooltip>
        </q-icon>
        <q-icon
          v-if="props.row.state == null"
          size="md"
          name="play_arrow"
          color="warning"
        >
          <q-tooltip>Próximo</q-tooltip>
        </q-icon>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { ref } from 'vue'

const addlabel = 'Agregar'
export default {
  props: {
    columns: Array,
    title: String,
    rows: Array,
    addFunction: Function,
    editFunction: Function,
    deleteFunction: Function,
  },
  setup() {
    const filter = ref('')
    return {
      addlabel,
      selected: ref([]),
      filter,
    }
  },
  methods: {
    load_details(item) {
      this.$router.push(`/equipments/${item.id}`)
    },
  },
}
</script>
