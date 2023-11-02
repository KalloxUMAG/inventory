<template>
  <div
    class="day-cell q-pa-0"
    :class="{
      today: day.isToday,
      'current-month': day.isCurrentMonth,
      weekend: day.isWeekEnd,
      'selected-day': isDaySelected,
    }"
    @click="showDayOptions"
  >
    <div class="d-flex justify-content-start">
      <p class="day-number">{{ day.date.format("D") }}</p>
    </div>
    <div class="event-grid">
      <event-card
        v-for="(event, index) in day.events.slice(0, 3)"
        :key="event.code"
        :event="event"
        role="button"
        :day-date="day.date"
        :is-day-selected="isDaySelected"
        :class="`event-space-${index + 1}`"
      >
      </event-card>
    </div>
    <div v-if="day.events.length > 3" class="float-right">
      ...
      <q-badge color="info">{{ day.events.length - 3 }} +</q-badge>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, toRefs } from "vue";
import EventCard from "./EventCard.vue";

const isDaySelected = ref(false);

const props = defineProps({
  day: {
    type: Object,
    required: false,
    default: () => ({}),
  },
  selectedDay: {
    type: Object,
    required: false,
    default: () => ({}),
  },
});

const { day, selectedDay } = toRefs(props);

const emit = defineEmits(["day-selected"]);

watch(
  selectedDay,
  (value) => {
    isDaySelected.value = value?.dayDate.date === day.value.date;
  },
  { immediate: true, deep: true }
);

const showDayOptions = () => {
  isDaySelected.value = true;
  emit("day-selected", { dayDate: day.value });
};
</script>

<style scoped>
.day-cell {
  flex: 1;
  min-height: 140px;

  border-right: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  background: rgba(147, 147, 147, 0.1);
}

.day-number {
  text-align: right;
  color: rgba(0, 0, 0, 0.25);
  font-size: 1em;
  padding: 5px;
}

.current-month {
  background: #fff;
}

.current-month p {
  color: rgba(0, 0, 0, 0.5);
  font-size: 1.5em;
}

.selected-day p {
  font-size: 2em;
  font-weight: bolder;
}

.weekend p {
  color: rgba(210, 2, 2, 0.6);
}

.today {
  background-color: #e8fde7;
}

.today p {
  font-size: 2em;
  font-weight: bolder;
  color: #4caf50;
}

.event-grid {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
}

.event-space-1 {
  grid-row: 1;
}

.event-space-2 {
  grid-row: 2;
}

.event-space-3 {
  grid-row: 3;
}

.event-card {
  grid-column: span 1; /* Por defecto, cada evento ocupa un solo día. */
}
</style>
