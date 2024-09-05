<template>
  <q-card class="col-12 no-shadow card-style" bordered>
    <q-card-section class="q-pa-xs">
      <q-table
        :grid="$q.screen.xs"
        row-key="id"
        :columns="loansColumns"
        :rows="loans"
        no-data-label="No hay registros para mostrar"
        rows-per-page-label="Registros por pagina"
        flat
        bordered
        no-wrap
        :filter="filter"
        class="card-style"
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
          </q-tr>
        </template>
        <template #body-cell="props">
          <q-td
            :props="props"
          >
            {{ props.value }}
          </q-td>
        </template>
        <template #body-cell-state="props">
          <q-td :props="props" auto-width>
            <!-- Mostrar icono si state es false, de lo contrario mostrar texto normal -->
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'
import { loansColumns } from 'src/constants/columns'
import { getLoans } from 'src/services'

const filter = ref('')
const loans = ref([])

const $q = useQuasar()

async function getLoansData() {
  loans.value = await getLoans()
}

onMounted(() => {
  getLoansData()
})
</script>
