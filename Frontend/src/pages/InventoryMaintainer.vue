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
    <section class="col-12 row">
      <section class="col-9">
        <calendar
          :first-day="1"
          :all-events="events"
          @day-selected="handleSelectDay"
          @change-month="handleChangeMonth"
        />
      </section>
      <section v-if="selectDay" class="col-3">
        <div>
          <schedule
            :selected-day="selectDay"
            @show-modal="handleShowModal"
            @new="handleShowModal"
          />
        </div>
      </section>
    </section>
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

const AddSupply = (supply) => {
  events.value.push({
    supply,
    date: dayjs(supply.date.from, "DD-MM-YYYY").toDate(),
    status: 6,
  });

  events.value.push({
    supply,
    date: dayjs(supply.date.to, "DD-MM-YYYY").toDate(),
    status: 3,
  });

  console.log(supply.date);
  console.log(supply, "supply");
  selectDay.value = null;
};
</script>
