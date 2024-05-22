<template>
  <div class="week-row" @click="showWeekNumber">
    <div v-if="showWeekNumberFlag" class="week-number">
      Semana {{ week[0].date.format("w") }}
    </div>
    <Day
      v-for="(day, index) in week"
      :key="index"
      :day="day"
      :selected-day="selectedDay"
      :selection="selection"
      @day-selected="handleSelectDay"
    />
  </div>
</template>

<script setup>
import { defineEmits, ref, toRefs, watch } from 'vue'
import Day from './Day.vue'

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
  selection: {
    type: Object,
    required: false,
    default: () => ({}),
  },
})

const emit = defineEmits(['day-selected', 'week-selected'])

const showWeekNumberFlag = ref(false)

const { week, selectedDay, selectedWeek } = toRefs(props)

watch(
  selectedWeek,
  (value) => {
    showWeekNumberFlag.value = value?.weekDate === week.value[0].date
  },
  { immediate: true },
)

function handleSelectDay(payload) {
  emit('day-selected', payload)
}

function showWeekNumber() {
  emit('week-selected', { weekDate: week.value[0].date })
}
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
