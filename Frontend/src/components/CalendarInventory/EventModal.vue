<template>
  <q-dialog v-model="showModal">
    <q-card style="width: 700px; max-width: 80vw">
      <q-card-section>
        <div class="text-h5 text-weight-bold">{{ title }}</div>
      </q-card-section>
      <q-card-section>
        <q-form ref="formEquipmentRef" @submit="handleSendNewForm">
          <div class="row justify-between q-mx-auto">
            <p class="col-12 text-h6 q-mb-md">Usuario a realizar préstamo</p>
            <div class="row col-12 justify-between q-mb-md">
              <q-input
                class="col-12 col-md-8 q-pb-none"
                v-model="card.user.fullname"
                standout="bg-teal text-white"
                label="Nombre"
                readonly
                :rules="[(val) => !!val || 'Este campo es obligatorio']"
              />
              <q-btn
                icon="search"
                @click="showModalSearch = true"
                class="col-12 col-md-3"
              >
                Buscar Usuario</q-btn
              >
            </div>

            <div @click="toggleDatePopup" class="col-12 row q-pt-md">
              <p class="col-12 text-h6 q-mb-md">
                Ingrese el rango de fechas para el préstamo
              </p>
              <div class="col-11 text-h6 q-mb-md">
                <q-input
                  class="q-pb-none"
                  standout="bg-teal text-white"
                  :label="
                    card.date
                      ? `Desde: ${card.date.from}, Hasta : ${card.date.to}`
                      : 'Ingrese rango de fechas'
                  "
                  readonly
                  :error="card.date ?? true"
                  error-message="Este campo es obligatorio"
                >
                  <q-popup-proxy
                    cover
                    :breakpoint="600"
                    @before-show="updateProxy"
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date
                      placeholder="DD-MM-AAAA"
                      title="Ingrese rango"
                      v-model="card.date"
                      range
                      today-btn
                      :locale="myLocale"
                      mask="DD-MM-YYYY"
                      color="primary"
                      :rules="[(val) => !!val || 'Este campo es obligatorio']"
                    >
                      <div class="row items-center justify-end q-gutter-sm">
                        <q-btn
                          label="Cancel"
                          color="primary"
                          flat
                          v-close-popup
                        />
                        <q-btn
                          label="OK"
                          color="primary"
                          flat
                          @click="save"
                          v-close-popup
                        />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-input>
              </div>
              <div class="col-1 row flex-center q-mb-md">
                <q-btn
                  ref="datePopupRef"
                  icon="event"
                  square
                  class="full-height"
                  color="primary"
                >
                  <q-popup-proxy
                    @before-show="updateProxy"
                    cover
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date
                      placeholder="DD-MM-AAAA"
                      title="Ingrese rango"
                      v-model="card.date"
                      range
                      today-btn
                      :locale="myLocale"
                      mask="DD-MM-YYYY"
                      color="primary"
                      :rules="[(val) => !!val || 'Este campo es obligatorio']"
                    >
                      <div class="row items-center justify-end q-gutter-sm">
                        <q-btn
                          label="Cancel"
                          color="primary"
                          flat
                          v-close-popup
                        />
                        <q-btn
                          label="OK"
                          color="primary"
                          flat
                          @click="save"
                          v-close-popup
                        />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-btn>
              </div>
            </div>

            <div class="col-12 row q-pt-md">
              <p class="col-12 text-h6 q-mb-md">Ingrese el equipo a prestar</p>
              <div class="col-12 text-h6 q-mb-md">
                <q-select
                  class="col-12 col-md-12 q-mb-md"
                  v-model="card.consumables"
                  standout="bg-teal text-white"
                  :options="types"
                  label="Equipos Disponibles"
                  :readonly="card.date ?? true"
                  :rules="[(val) => !!val || 'Este campo es obligatorio']"
                >
                  <q-tooltip
                    v-if="card.date === null"
                    class="bg-secondary text-body2"
                    anchor="top middle"
                    self="bottom middle"
                    transition-show="flip-right"
                    transition-hide="flip-left"
                    :offset="[10, 10]"
                  >
                    Ingrese la el rango de fechas para el préstamo
                  </q-tooltip>
                </q-select>
              </div>
            </div>
          </div>
          <div class="row justify-end">
            <q-btn label="Cancelar" @click="cancel" />
            <q-btn
              label="Guardar"
              class="q-mx-sm"
              type="submit"
              color="primary"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
  <modal-search-user
    @close="showModalSearch = false"
    :showModalSearch="showModalSearch"
    @selectedUser="handleSelectedUser"
  />
</template>

<script setup>
import { ref, watch, toRefs, onMounted, computed } from "vue";
import ModalSearchUser from "../commons/ModalSearchUser.vue";
import { useEquipmentStore } from "stores";
import { useQuasar } from "quasar";
import dayjs from "dayjs";
import "dayjs/locale/es";
dayjs.locale("es");

const equipmentStore = useEquipmentStore();
const $q = useQuasar();

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
const card = ref({
  user: {
    id: "",
    email: "",
    fullname: "",
  },
  consumables: "",
  quantity: 0,
  date: null,
});
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
const showModalSearch = ref(false);

const datePopupRef = ref(null);
const formEquipmentRef = ref(null);

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

watch(
  () => card.value.date,
  (newVal) => {
    if (newVal) {
      card.value.consumables = "";
      formEquipmentRef.value.resetValidation();
      availableEquipment();
    }
  },
  { immediate: false, deep: true }
);

const handleSendNewForm = async () => {
  const { name, dni, consumables, quantity, date, user, ...rest } = card.value;

  emit("create", {
    name,
    dni,
    consumables,
    quantity,
    date,
    user,
  });

  cancel();
};

const cancel = () => {
  emit("close");
};

const handleSelectedUser = (selectedUser) => {
  showModalSearch.value = false;
  card.value = {
    ...card.value,
    user: {
      id: selectedUser.id,
      email: selectedUser.email,
      fullname: selectedUser.fullname,
    },
  };
};

const toggleDatePopup = () => {
  if (datePopupRef.value) {
    datePopupRef.value.click();
  }
};

const availableEquipment = async () => {
  try {
    const response = await equipmentStore.fetchEquipmentAvailable({
      start_date: dayjs(card.value.date.from, "DD-MM-YYYY").format(
        "YYYY-MM-DD"
      ),
      end_date: dayjs(card.value.date.to, "DD-MM-YYYY").format("YYYY-MM-DD"),
    });
    if (response && Array.isArray(response)) {
      types.value = response.map((equip) => ({
        label: equip.name,
        value: equip.id,
        description: equip.observation || "Sin descripción",
        category: equip.stage_id,
        available: equip.available,
        dateEnd: equip.dateEnd || null,
      }));
    } else {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message:
          "No se encontraron equipamientos disponibles para este rango de fechas",
      });
    }
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la marca: " + error,
    });
  }
};
</script>

<style scoped></style>
