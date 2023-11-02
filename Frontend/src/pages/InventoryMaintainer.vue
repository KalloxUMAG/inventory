<template>
  <div class="row q-pa-md">
    <section class="col-12">
      <div class="row justify-between items-center">
        <div class="row items-center">
          <q-icon name="fas fa-calendar-days" size="2em" />
          <h5 class="q-ma-sm">Mantenedor de inventario</h5>
        </div>
        <div>
          <div v-if="showModal">
            <eventModal
              :show-modal="showModal"
              :event="event"
              :title="event?.title ?? 'Insumo'"
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
        >
        </q-btn>
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
import { ref } from "vue";
import calendar from "../components/CalendarInventory/Calendar.vue";
import schedule from "../components/CalendarInventory/Schedule.vue";
import eventModal from "../components/CalendarInventory/EventModal.vue";
import dayjs from "dayjs";
dayjs.locale("es");

const selectDay = ref(null);
const events = ref([]);
const event = ref(null);
const previousMonth = ref(null);
const nextMonth = ref(null);
const showModal = ref(false);
const filterType = ref([
  {
    label: "Prestamos",
    value: 1,
    description: "Ver Dias de Prestamos",
    category: "1",
  },
  {
    label: "Devoluciones",
    value: 2,
    description: "Ver Dias de devoluciones",
    category: "2",
  },
  {
    label: "Equipamientos en préstamo ",
    value: 3,
    description: "Ver equipamiento prestado",
    category: "3",
  },
]);
const selectionTables = ref({});

const handleSelectDay = (day) => {
  selectDay.value = day;
};

const handleChangeMonth = (month) => {
  nextMonth.value = month.clone().add(5, "week").format("DD/MM/YYYY");
  previousMonth.value = month.clone().subtract(3, "week").format("DD/MM/YYYY");
};

const handleShowModal = () => {
  showModal.value = true;
};

const hideModal = () => {
  showModal.value = false;
};

let localId = 1;
const AddSupply = (supply) => {
  const startDate = dayjs(supply.date.from, "DD-MM-YYYY");
  const endDate = dayjs(supply.date.to, "DD-MM-YYYY");

  for (
    let date = startDate;
    date.isBefore(endDate) || date.isSame(endDate);
    date = date.add(1, "day")
  ) {
    events.value.push({
      id: localId,
      supply,
      date: date.toDate(),
      status: date.isSame(startDate) ? 6 : 3,
      isStarter: date.isSame(startDate),
      isEnd: date.isSame(endDate),
      showExtend: false,
    });
  }
  localId++;
  selectDay.value = null;
};

const hideSelectDay = () => {
  selectDay.value = null;
};

const handleSelectedIdsChanged = (newSelectedIds) => {
  const selectedDayKey = selectDay.value.dayDate.weekDay;

  const deselectedIds =
    selectionTables.value[selectedDayKey]?.filter(
      (id) => !newSelectedIds.includes(id)
    ) || [];

  events.value.forEach((event) => {
    if (deselectedIds.includes(event.id)) {
      event.showExtend = false;
    }
  });

  const selectedIds =
    newSelectedIds.filter(
      (id) => !selectionTables.value[selectedDayKey]?.includes(id)
    ) || [];

  events.value.forEach((event) => {
    if (selectedIds.includes(event.id)) {
      event.showExtend = true;
    }
  });

  selectionTables.value[selectedDayKey] = newSelectedIds;
};
</script>
