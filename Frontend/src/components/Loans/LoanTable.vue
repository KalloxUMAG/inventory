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
        <template #body-cell-supplyName="props">
          <q-td :props="props" auto-width>
            <a :href="`/supplies/${props.row.supply_id}`">{{ props.row.supply_name }}</a>
          </q-td>
        </template>
        <template #body-cell-state="props">
          <q-td :props="props" auto-width>
            <!-- Mostrar icono si state es false, de lo contrario mostrar texto normal -->
            <q-chip v-if="props.row.state === 'devuelto'" color="teal" text-color="white" icon="check">
              Devuelto
            </q-chip>
            <q-chip v-if="props.row.state === 'pendiente'" color="red" text-color="white" icon="schedule">
              Pendiente
            </q-chip>
          </q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td :props="props" auto-width>
            <q-btn
              flat
              dense
              icon="edit"
              color="warning"
              @click="editLoan(props.row)"
            />
            <q-btn
              v-if="props.row.id != null"
              flat
              dense
              icon="delete"
              color="negative"
            />
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

import LoanEditFormModal from './LoanEditFormModal.vue'

const filter = ref('')
const loans = ref([])

const $q = useQuasar()

async function getLoansData() {
  loans.value = await getLoans()
}

function editLoan(loan) {
  $q.dialog({
    component: LoanEditFormModal,
    componentProps: {
      id: loan.id,
      group: loan.group_name,
      supply: loan.supply_name,
      lot: loan.lot_number,
      loanDate: loan.start_date,
      returnDate: loan.end_date,
      state: loan.state,
      description: loan.description,
    },
  }).onOk(async () => {
    await getLoansData()
  })
}

onMounted(() => {
  getLoansData()
})
</script>
