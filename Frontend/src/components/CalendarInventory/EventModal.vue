<template>
  <q-dialog v-model="showModal">
    <q-card style="width: 700px; max-width: 80vw">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="handleSendNewForm">
          <div class="q-gutter-md row justify-start">
            <q-input
              class="col-12 col-md-8"
              v-model="card.name"
              standout="bg-teal text-white"
              label="Nombre"
            />
            <q-input
              class="col-12 col-md-8"
              v-model="card.dni"
              standout="bg-teal text-white"
              label="RUT"
            />
            <q-select
              class="col-12 col-md-8"
              v-model="card.consumables"
              standout="bg-teal text-white"
              :options="types"
              label="Insumo"
            />
            <div class="col-11 row">
              <p class="col-12">Cantidad</p>
              <q-slider
                class="col-12 q-mx-xs"
                v-model="card.quantity"
                marker-labels
                :min="1"
                :max="maxQuantity"
              />
            </div>

            <div class="col-12 row">
              <p class="col-12">Fecha de préstamo</p>
              <q-date
                placeholder="DD-MM-AAAA"
                title="Ingrese rango"
                v-model="card.date"
                range
                today-btn
                :locale="myLocale"
                mask="DD-MM-YYYY"
              />
            </div>
          </div>
          <div class="row justify-end">
            <q-btn label="Cancelar" @click="cancel" />
            <q-btn
              label="Guardar"
              class="q-mx-xs"
              type="submit"
              color="primary"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch, toRefs, onMounted, computed } from "vue";

const props = defineProps({
  showModal: {
    type: Boolean,
    required: true,
    default: false,
  },
  title: String,
  event: Object,
});

const { showModal, uniqueKey, title, event } = toRefs(props);

const emit = defineEmits(["close", "create"]);

const show = ref(true);
const card = ref({});
const types = ref([]);
const myLocale = ref({
  /* starting with Sunday */
  days: "Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado".split("_"),
  daysShort: "Dom_Lun_Mar_Mié_Jue_Vie_Sáb".split("_"),
  months:
    "Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split(
      "_"
    ),
  monthsShort: "Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic".split("_"),
  firstDayOfWeek: 1,
  format24h: true,
  pluralDay: "dias",
});

onMounted(() => {
  types.value = [
    {
      label: "Insumo 1",
      value: 1,
      description: "Descripción insumo 1",
      category: "1",
      quantity: 10,
    },
    {
      label: "Insumo 2",
      value: 2,
      description: "Descripción insumo 2",
      category: "2",
      quantity: 5,
    },
    {
      label: "Insumo 3",
      value: 3,
      description: "Descripción insumo 3",
      category: "3",
      quantity: 4,
    },
  ];
});

//computed
const maxQuantity = computed(() => {
  return card.value.consumables?.quantity ?? 1;
});

watch(
  () => props.showModal,
  (newVal) => {
    show.value = newVal;
  }
);

watch(
  () => props.event,
  (newVal) => {
    if (newVal) card.value = { ...newVal };
  },
  { immediate: true, deep: true }
);

const handleSendNewForm = async () => {
  const { name, dni, consumables, quantity, date, ...rest } = card.value;

  emit("create", {
    name,
    dni,
    consumables,
    quantity,
    date,
  });

  cancel();
};

const cancel = () => {
  emit("close");
};
</script>
