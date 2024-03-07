<template>
  <div class="schedule">
    <div>
      <div class="text-right">
        <q-btn
          color="negative"
          unelevated
          dense
          icon="close"
          @click="closeSelectedDay"
        />
      </div>
    </div>
    <section>
      <div class="q-pa-md">
        <div class="row q-gutter-md">
          <div class="col row justify-center items-end">
            <div class="text-h1">
              {{ selectedDay.dayDate.date.format("D") }}
            </div>
          </div>
          <div class="col">
            <div class="text-h4">
              {{ selectedDay.dayDate.date.format("MMMM YYYY") }}
            </div>
            <div class="text-h6">
              {{ selectedDay.dayDate.date.format("dddd") }}
            </div>
          </div>
        </div>
      </div>
    </section>
    <section>
      <div class="q-pa-md">
        <div class="q-mb-md">
          <h5>Prestamos</h5>
          <q-table
            :rows="loans"
            :columns="columns"
            class="bg-info text-white"
            :row-key="(row) => `${row.supply.name}-${row.supply.dni}`"
            flat
            bordered
            selection="multiple"
            v-model:selected="selectionTables"
          />
        </div>
        <div>
          <h5>Devoluciones</h5>
          <q-table
            :rows="returns"
            :columns="columns"
            class="bg-positive text-white"
            :row-key="(row) => `${row.supply.name}-${row.supply.dni}`"
            flat
            bordered
            selection="multiple"
            v-model:selected="selectionTables"
          />
        </div>
        <div>
          <h5>Instrumentos en Préstamo</h5>
          <q-table
            :rows="inLoans"
            :columns="columns"
            class="bg-warning text-white"
            :row-key="(row) => `${row.supply.name}-${row.supply.dni}`"
            flat
            bordered
            selection="multiple"
            v-model:selected="selectionTables"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed } from "vue";
import dayjs from "dayjs";
dayjs.locale("es");

const props = defineProps({
  selectedDay: {
    type: Object,
    required: false,
    default: () => ({}),
  },
});

const selectionTables = ref([]);
const columns = [
  {
    name: "user_fullname",
    required: true,
    label: "Nombre",
    align: "left",
    field: (row) => row.supply.user_fullname,
  },
  {
    name: "user_email",
    required: true,
    label: "Email",
    align: "left",
    field: (row) => row.supply.user_email,
  },
  {
    name: "equipment_name",
    required: true,
    label: "Equipo",
    align: "left",
    field: (row) => row.supply.equipment_name,
  },
  {
    name: "loan_start_date",
    required: true,
    label: "Fecha Inicio",
    align: "left",
    field: (row) => row.supply.loan_start_date,
  },
  {
    name: "loan_end_date",
    required: true,
    label: "Fecha Termino",
    align: "left",
    field: (row) => row.supply.loan_end_date,
  },
];

const closeSelectedDay = () => {
  emit("close-selected-day");
};

const emit = defineEmits(["new", "show-modal", "close-selected-day"]);

const selectedIds = computed(() => {
  const combinedSelections = [...(selectionTables.value || [])];
  return [...new Set(combinedSelections.map((event) => event.id))];
});

const loans = computed(() =>
  props.selectedDay.dayDate.events.length > 0
    ? props.selectedDay.dayDate.events?.filter((event) => event.isStarter)
    : []
);
const returns = computed(() =>
  props.selectedDay.dayDate.events.length > 0
    ? props.selectedDay.dayDate.events?.filter((event) => event.isEnd)
    : []
);
const inLoans = computed(() =>
  props.selectedDay.dayDate.events?.length > 0
    ? props.selectedDay.dayDate?.events
    : []
);

watch(selectedIds, (newIds, oldIds) => {
  emit("selected-ids-changed", newIds);
});
</script>

<style scoped>
.schedule {
  background-color: #fff;
  border-radius: 10px;
}
</style>
