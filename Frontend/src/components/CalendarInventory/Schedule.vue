<template>
  <div class="schedule">
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
            row-key="name"
          />
        </div>
        <div>
          <h5>Devoluciones</h5>
          <q-table
            :rows="returns"
            :columns="columns"
            class="bg-positive text-white"
            row-key="name"
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

const columns = [
  {
    name: "name",
    required: true,
    label: "Nombre",
    align: "left",
    field: (row) => row.supply.name,
  },
  {
    name: "dni",
    required: true,
    label: "Rut",
    align: "left",
    field: (row) => row.supply.dni,
  },
  {
    name: "consumables",
    required: true,
    label: "Insumo",
    align: "left",
    field: (row) => row.supply.consumables.label,
  },
  {
    name: "date",
    required: true,
    label: "Fecha",
    align: "left",
    field: (row) => dayjs(row.date).format("DD/MM/YYYY"),
  },
];

const emit = defineEmits(["new", "show-modal"]);

const loans = computed(() =>
  props.selectedDay.dayDate.events.length > 0
    ? props.selectedDay.dayDate.events?.filter((event) => event.status === 6)
    : []
);
const returns = computed(() =>
  props.selectedDay.dayDate.events.length > 0
    ? props.selectedDay.dayDate.events?.filter((event) => event.status === 3)
    : []
);
</script>

<style scoped>
.schedule {
  background-color: #fff;
  border-radius: 10px;
}
</style>
