<template>
  <div class="">
    <div v-if="loading">
      Loading...
    </div>
    <div v-if="error" class="error" />
    <div class="">
      <div>
        <CalendarHeader
          :current-month="currentMonth"
          :locale="appLocale"
          @change-month="changeMonth"
        />
        <div class="full-calendar-body">
          <div class="weeks">
            <strong v-for="(dayIndex, index) in 7" :key="index" class="week">
              {{ weekDayName(dayIndex - 1, firstDay, appLocale) }}
            </strong>
          </div>
          <div ref="dates" class="dates">
            <Week
              v-for="(week, index) in Weeks"
              :key="index"
              :week="week"
              :selected-day="selectedDay"
              :selected-week="selectedWeek"
              :selection="selection"
              @day-selected="handleSelectDay"
              @week-selected="handleSelectWeek"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineEmits, onMounted, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import advancedFormat from 'dayjs/plugin/advancedFormat'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import localeData from 'dayjs/plugin/localeData'
import weekOfYear from 'dayjs/plugin/weekOfYear'
import isoWeek from 'dayjs/plugin/isoWeek'
import Week from './Week.vue'
import CalendarHeader from './CalendarHeader.vue'
import 'dayjs/locale/es'

const props = defineProps({
  allEvents: {
    type: Array,
    default() {
      return []
    },
  },
  firstDay: {
    type: [Number, String],
    validator(val) {
      const res = Number.parseInt(val)
      return res >= 0 && res <= 6
    },
    default: 0,
  },
  selection: {
    type: Object,
    default() {
      return {}
    },
  },
})
const emit = defineEmits(['change-month', 'day-selected'])
// importa el idioma español

dayjs.extend(advancedFormat)
dayjs.extend(customParseFormat)
dayjs.extend(localeData)
dayjs.extend(weekOfYear)
dayjs.extend(isoWeek)

dayjs.locale('es')

const loading = ref(true)
const error = ref(null)
const currentMonth = ref(dayjs().startOf('month'))
const appLocale = ref('es')
const selectedDay = ref(null)
const selectedWeek = ref(null)

const { allEvents, firstDay } = toRefs(props)

function weekDayName(weekday, firstDay) {
  firstDay = Number.parseInt(firstDay)
  const day = (weekday + firstDay + 7) % 7 // Agrega 6 antes del módulo 7
  const weekDays = [
    'Domingo',
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
  ]
  return weekDays[day]
}

const Weeks = computed(() => {
  emit('change-month', currentMonth.value)
  let monthDayjsObject = getMonthViewStartDate(
    currentMonth.value,
    firstDay.value,
  )
  const weeks = []
  const daysInCurrentMonth = currentMonth.value.daysInMonth()
  for (let weekIndex = 0; weekIndex < 6; weekIndex++) {
    const week = []
    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
      week.push(getDayObject(monthDayjsObject, dayIndex))
      monthDayjsObject = monthDayjsObject.add(1, 'day')
    }
    weeks.push(week)
  }
  const diff = daysInCurrentMonth - weeks[4][6].date.format('D')
  if (diff > 0 && diff < 3) {
    const week = []
    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
      week.push(getDayObject(monthDayjsObject, dayIndex))
      monthDayjsObject = monthDayjsObject.add(1, 'day')
    }
    weeks.push(week)
  }
  return weeks
})

const events = computed(() => allEvents.value)

onMounted(() => {
  loading.value = false
})

function handleSelectDay(payload) {
  if (payload.dayDate.date !== selectedDay.value?.date) {
    selectedDay.value = payload
    emit('day-selected', payload)
  }
}

function handleSelectWeek(payload) {
  if (payload.weekDate !== selectedWeek.value?.[0]?.date)
    selectedWeek.value = payload
}

function changeMonth(payload) {
  selectedDay.value = null
  currentMonth.value = payload
}

function getEvents(date) {
  return events.value.filter((event) => {
    return date.isSame(event.date, 'day') ? event : null
  })
}

function getMonthViewStartDate(date, firstDay) {
  const start = dayjs(date).locale(appLocale)
  const startOfMonth = start.startOf('month')

  let diffDays = startOfMonth.day() === 0 ? 6 : startOfMonth.day() - 1
  if (diffDays < 0)
    diffDays += 7

  const resultDate = startOfMonth.subtract(diffDays, 'day')
  return resultDate
}

function getDayObject(monthDayjsObject, dayIndex) {
  return {
    isToday: monthDayjsObject.isSame(dayjs(), 'day'),
    isCurrentMonth: monthDayjsObject.isSame(currentMonth.value, 'month'),
    weekDay: dayIndex,
    isWeekEnd: dayIndex === 6 || dayIndex === 5,
    date: monthDayjsObject,
    events: getEvents(monthDayjsObject),
  }
}
</script>

<style scoped>
ul,
p {
  margin: 0;
  padding: 0;
}

.full-calendar-body {
  margin-top: 20px;
}

.weeks {
  display: flex;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  border-left: 1px solid #e0e0e0;
}

.week {
  flex: 1;
  padding: 5px;
  text-align: center;
  border-right: 1px solid #e0e0e0;
}

.dates {
  position: relative;
}
</style>
