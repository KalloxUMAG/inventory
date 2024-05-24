<template>
  <PageTitle title="Proveedores" icon="store" />
  <q-card class="no-shadow bg-transparent">
    <q-card-section class="q-pl-none col-12">
      <div class="text-subtitle1 q-pl-md space-between">
        Lista de Proveedores
        <div class="actions-buttons">
          <q-input
            v-model="filter"
            outlined
            bg-color="white"
            dense
            debounce="300"
            placeholder="Buscar"
          >
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-btn
            class="add-btn q-mr-sm"
            to="/suppliers/new_supplier"
            icon="add_business"
            label="Agregar"
            flat
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        row-key="id"
        :columns="suppliersColumns"
        :rows="suppliers"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        flat
        bordered
        wrap-cells
        :filter="filter"
        class="card-style"
        @row-click="rowClicker"
      >
        <template #header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              class="text-italic table-header" :class="[col.additionalClass]"
            >
              {{ col.label }}
            </q-th>
            <q-th auto-width>
              Contactos
            </q-th>
          </q-tr>
        </template>
        <template #body="props">
          <q-tr :props="props" class="item-row">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              @click="rowClicker(props.row)"
            >
              {{ col.value }}
            </q-td>
            <q-td auto-width>
              <q-btn size="sm" align="between" color="accent" flat :icon-right="props.expand ? 'expand_less' : 'expand_more'" @click="props.expand = !props.expand" />
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td class="subtable" colspan="100%">
              <q-table
                :rows="props.row.contacts"
                :columns="suppliersContactsColumns"
                row-key="id"
                flat
                no-wrap
                hide-bottom
                card-class="bg-grey-1 text-grey-8"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import PageTitle from 'src/components/commons/PageTitle.vue'
import { suppliersColumns, suppliersContactsColumns } from 'src/constants/columns'

import { getSuppliersFull } from 'src/services'

const router = useRouter()

const suppliers = ref([])
const filter = ref('')

const detail_query = '/suppliers/'

async function getSuppliersData() {
  suppliers.value = await getSuppliersFull()
}

function rowClicker(row) {
  const item = row.id
  router.push(detail_query + item)
}

onMounted(() => {
  getSuppliersData()
})
</script>

<style scoped>
.card-style {
  border-radius: 12px;
}

.space-between {
  display: flex;
  justify-content: space-between;
}

.actions-buttons {
  display: inline-flex;
  gap: 10px;

  .add-btn {
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
}
.image-visor {
  border: none !important;
  padding: 0;
}

.width-300 {
  width: 300px;
}
.subtable{
  padding: 0;
}
.item-row{
  cursor: pointer;
}
</style>
