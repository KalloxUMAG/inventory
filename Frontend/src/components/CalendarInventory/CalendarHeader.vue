<template>
  <div class="row flex flex-center justify-center">
    <div class="col-12 flex flex-center justify-center">
      <q-btn-group>
        <q-btn icon="fas fa-fast-backward" @click.stop="goPrevYear" />
        <q-btn icon="fas fa-step-backward" @click.stop="goPrev" />
        <q-btn
          label="Hoy"
          color="white"
          text-color="primary"
          @click.stop="goToday"
        />
        <q-btn icon="fas fa-step-forward" @click.stop="goNext" />
        <q-btn icon="fas fa-fast-forward" @click.stop="goNextYear" />
      </q-btn-group>
    </div>
    <div class="col-12 text-center text-h5 q-my-md">
      <strong>{{ title }}</strong>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, toRefs } from "vue";
import dayjs from "dayjs";
import "dayjs/locale/es";
dayjs.locale("es");

const props = defineProps({
  currentMonth: {
    type: Object,
    required: true,
  },
  locale: {
    type: String,
    default: "es",
  },
});

const { currentMonth, locale } = toRefs(props);
const emit = defineEmits(["change-month"]);

const title = computed(() => {
  if (!currentMonth.value) return;
  return currentMonth.value.locale(locale.value).format("MMMM YYYY");
});

const goPrev = () => {
  const payload = dayjs(currentMonth.value)
    .subtract(1, "months")
    .startOf("month");
  emit("change-month", payload);
};

const goNext = () => {
  const payload = dayjs(currentMonth.value).add(1, "months").startOf("month");
  emit("change-month", payload);
};

const goNextYear = () => {
  const payload = dayjs(currentMonth.value).add(12, "months").startOf("month");
  emit("change-month", payload);
};

const goPrevYear = () => {
  const payload = dayjs(currentMonth.value)
    .subtract(12, "months")
    .startOf("month");
  emit("change-month", payload);
};

const goToday = () => {
  emit("change-month", dayjs());
};
</script>

<style scoped>
.full-calendar-header {
  display: flex;
  align-items: center;
}

.header-center {
  flex: 3;
  text-align: center;
}

.month-title {
  text-align: center;
  font-size: 1.5em;
  font-weight: bolder;
}

.language-select {
  display: inline-block;
  width: 50%;
}
</style>
