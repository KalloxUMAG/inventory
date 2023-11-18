<template>
  <div class="row">
    <q-dialog
      v-model="show"
      @hide="emitCloseEvent"
      class="col-12 col-md-8 col-lg-6 col-xl-4"
      ref="serachUser"
      square
      transition-show
    >
      <q-card>
        <q-card-section class="q-pa-lg">
          <h5 class="q-my-none text-bold">Buscar Usuarios</h5>
          <q-form @submit="submitForm" @reset="onReset" class="row">
            <q-input
              v-model="name"
              label="Nombre"
              class="col-12 col-md-6 q-pr-sm"
              :rules="[
                (val) =>
                  !!val ||
                  !!email ||
                  'Debes ingresar al menos un nombre o email',
              ]"
            />
            <q-input
              v-model="email"
              label="Email"
              class="col-12 col-md-6"
              :rules="[
                (val) =>
                  !!val ||
                  !!name ||
                  'Debes ingresar al menos un nombre o email',
              ]"
            />
            <div class="col-12 q-my-sm q-mt-lg">
              <q-btn
                label="Buscar"
                color="primary"
                icon-right="search"
                type="submit"
                size="lg"
                class="full-width"
              />
            </div>
          </q-form>

          <div>
            <h5 class="q-mb-sm">Seleccione un usuario</h5>
            <q-table
              :rows="users"
              :columns="columns"
              row-key="email"
              no-data-label="No hay registros para mostrar"
              @row-click="
                (evt, row, index) => handleSelectedUser(evt, row, index)
              "
              v-model:selected="selectedUser"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, defineProps, watch, defineEmits, computed } from "vue";
import { useQuasar } from "quasar";
import { useUserStore } from "stores";

const $q = useQuasar();
const userStore = useUserStore();

const name = ref("");
const email = ref("");
const users = ref([]);
const selectedUser = ref([]);
const show = ref(false);

const emit = defineEmits(["close", "selectedUser"]);

const emitCloseEvent = () => {
  emit("close", false);
};

const columns = [
  {
    name: "fullname",
    required: true,
    label: "Nombre Completo",
    align: "left",
    field: (row) => row.fullname,
  },
  {
    name: "email",
    required: true,
    label: "Email",
    align: "left",
    field: (row) => row.email,
  },
];

const props = defineProps({
  showModalSearch: Boolean,
});

watch(
  () => props.showModalSearch,
  (newVal) => {
    show.value = newVal;
  }
);

const submitForm = async () => {
  try {
    const response = await userStore.fetchUser({
      fullname: name.value,
      email: email.value,
    });
    if (response && Array.isArray(response)) {
      users.value = response;
    } else {
      users.value = [];
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

const onReset = () => {
  name.value = "";
  email.value = "";
};

const handleSelectedUser = (evt, row, index) => {
  onReset();
  users.value = [];

  emit("selectedUser", row);
};
</script>
