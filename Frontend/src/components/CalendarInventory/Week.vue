<template>
  <div class="week-row" @click="showWeekNumber">
    <div v-if="showWeekNumberFlag" class="week-number">
      Semana {{ week[0].date.format("w") }}
    </div>
    <day
      v-for="(day, index) in week"
      :key="index"
      :day="day"
      :selected-day="selectedDay"
      @day-selected="handleSelectDay"
    ></day>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, toRefs } from "vue";
import Day from "./Day.vue";

const showWeekNumberFlag = ref(false);

const props = defineProps({
  week: {
    type: Array,
    required: true,
  },
  selectedDay: {
    type: Object,
    required: false,
    default: () => ({}),
  },
  selectedWeek: {
    type: Object,
    required: false,
    default: () => ({}),
  },
});
const { week, selectedDay, selectedWeek } = toRefs(props);

const emit = defineEmits(["day-selected", "week-selected"]);

watch(
  selectedWeek,
  (value) => {
    showWeekNumberFlag.value = value?.weekDate === week.value[0].date;
  },
  { immediate: true }
);

const handleSelectDay = (payload) => {
  emit("day-selected", payload);
};

const showWeekNumber = () => {
  emit("week-selected", { weekDate: week.value[0].date });
};
</script>

<style scoped>
.week-row {
  width: 100%;
  border-left: 1px solid #e0e0e0;
  display: flex;
  cursor: pointer;
}

.week-number {
  border: 1px solid #e1e1e1;
  border-right: 0px;
  border-radius: 5px 0 0 5px;
  background-color: #fafafa;
  text-align: right;
  position: absolute;
  width: 77px;
  left: -77px;
  padding: 8px 5px;
  cursor: pointer;
}
</style>
