<template>
  <div class="row q-pa-md">
    <section class="col-12">
      <div class="row justify-between items-center">
        <PageTitle title="Mantenedor de inventario" icon="calendar_month" />
        <div>
          <div v-if="showModal">
            <eventModal
              :show-modal="showModal"
              :event="event"
              :title="event?.title ?? 'Suministrar equipamiento'"
              @create="AddSupply"
              @close="hideModal"
            />
          </div>
        </div>
      </div>
    </section>
    <div class="col-12 row justify-end q-my-md">
      <div class="q-mr-md">
        <q-btn
          size="12px"
          color="white"
          text-color="primary"
          outline
          label="Agregar"
          @click="handleShowModal"
        />
      </div>
    </div>
    <div class="col-12 row">
      <!--
        <div :class="[selectDay ? 'col-7' : 'col-12', 'row']">
          <q-select
            class="col-12 col-md-8"
            standout="bg-teal text-white"
            :options="filterType"
            label="Ver"
          />
        </div>
      -->
      <div :class="[selectDay ? 'col-7' : 'col-12']">
        <calendar
          :first-day="1"
          :all-events="events"
          :selection="selectionTables"
          @day-selected="handleSelectDay"
          @change-month="handleChangeMonth"
        />
      </div>
      <div v-if="selectDay" class="col-5 q-px-sm">
        <div>
          <schedule
            :selected-day="selectDay"
            @selected-ids-changed="handleSelectedIdsChanged"
            @show-modal="handleShowModal"
            @new="handleShowModal"
            @close-selected-day="hideSelectDay"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import PageTitle from 'src/components/commons/PageTitle.vue'
import { useQuasar } from 'quasar'
import dayjs from 'dayjs'
import calendar from '../components/CalendarInventory/Calendar.vue'
import schedule from '../components/CalendarInventory/Schedule.vue'
import eventModal from '../components/CalendarInventory/EventModal.vue'
import { useLoanStore } from '../stores'

dayjs.locale('es')

const loanStore = useLoanStore()
const $q = useQuasar()

const selectDay = ref(null)
const events = ref([])
const event = ref(null)
const previousMonth = ref(null)
const nextMonth = ref(null)
const showModal = ref(false)
const filterType = ref([
  {
    label: 'Prestamos',
    value: 1,
    description: 'Ver Dias de Prestamos',
    category: '1',
  },
  {
    label: 'Devoluciones',
    value: 2,
    description: 'Ver Dias de devoluciones',
    category: '2',
  },
  {
    label: 'Equipamientos en préstamo ',
    value: 3,
    description: 'Ver equipamiento prestado',
    category: '3',
  },
])
const selectionTables = ref({})

function handleSelectDay(day) {
  selectDay.value = day
}

function handleChangeMonth(month) {
  nextMonth.value = month.clone().add(5, 'week').format('DD/MM/YYYY')
  previousMonth.value = month.clone().subtract(3, 'week').format('DD/MM/YYYY')
}

function handleShowModal() {
  showModal.value = true
}

function hideModal() {
  showModal.value = false
}

async function AddSupply(supply) {
  const body = {
    user_id: supply.user.id,
    equipment_id: supply.consumables.value,
    loan_start_date: dayjs(supply.date.from, 'DD-MM-YYYY')
      .startOf('day')
      .toISOString()
      .split('T')[0],
    loan_end_date: dayjs(supply.date.to, 'DD-MM-YYYY')
      .startOf('day')
      .toISOString()
      .split('T')[0],
  }
  try {
    if (supply.consumables.available) {
      const response = await loanStore.postLoanEquipment(body)
      if (response && Array.isArray(response)) {
        $q.notify({
          color: 'red-3',
          textColor: 'white',
          icon: 'error',
          message: 'Equipamiento Guardado',
        })
        fetchLoans()
      }
      else {
        $q.notify({
          color: 'red-3',
          textColor: 'white',
          icon: 'error',
          message:
            'No se encontraron equipamientos disponibles para este rango de fechas',
        })
        console.log('not founds')
      }
    }
    else {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: 'Este equipo no esta disponible para este rango de fechas',
      })
    }
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la marca: ${error}`,
    })
  }
}

function hideSelectDay() {
  selectDay.value = null
}

function handleSelectedIdsChanged(newSelectedIds) {
  const selectedDayKey = selectDay.value.dayDate.weekDay

  const deselectedIds
    = selectionTables.value[selectedDayKey]?.filter(
      id => !newSelectedIds.includes(id),
    ) || []

  events.value.forEach((event) => {
    if (deselectedIds.includes(event.id))
      event.showExtend = false
  })

  const selectedIds
    = newSelectedIds.filter(
      id => !selectionTables.value[selectedDayKey]?.includes(id),
    ) || []

  events.value.forEach((event) => {
    if (selectedIds.includes(event.id))
      event.showExtend = true
  })

  selectionTables.value[selectedDayKey] = newSelectedIds
}

async function fetchLoans() {
  try {
    const response = await loanStore.fetchLoan()
    if (response && Array.isArray(response)) {
      events.value = []
      loadLoans(response)
    }
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message:
        `No se pudieron obtener los equipamientos en prestamos: ${error}`,
    })
  }
}

function loadLoans(loans) {
  loans.forEach((loan) => {
    const startDate = dayjs(loan.loan_start_date)
    const endDate = dayjs(loan.loan_end_date)

    for (
      let date = startDate;
      date.isBefore(endDate) || date.isSame(endDate);
      date = date.add(1, 'day')
    ) {
      console.log(loan)
      events.value.push({
        id: loan.loan_id,
        supply: loan,
        date: date.toDate(),
        status: date.isSame(startDate) ? 6 : 3,
        isStarter: date.isSame(startDate),
        isEnd: date.isSame(endDate),
        showExtend: false,
      })
    }
  })
  selectDay.value = null
}

onMounted(() => {
  fetchLoans()
})
</script>
