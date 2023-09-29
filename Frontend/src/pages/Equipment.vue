<template>
  <q-page padding>
    <div v-if="equipment != null" class="row justify-center">
      <q-card class="my-card" flat bordered>
        <q-item class="row justify-center">
          <div class="text-h5">
            {{ equipment.name }} - {{ equipment.model_name }}
          </div>
        </q-item>
        <q-separator />
        <q-card-section horizontal>
          <!--Datos carrucel-->
          <q-card-section class="col-4">
            <Carousel v-if="img_api != null" :api_endpoint="img_api" />
          </q-card-section>
          <q-separator vertical />
          <!--Datos producto-->
          <q-card-section class="col">
            <div class="text-h5 q-mb-md text-center">
              Datos producto<q-btn
                class="q-ml-md glossy"
                icon="edit"
                color="positive"
                @click="editProduct"
              />
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Nombre:</div>
              <div class="col field-content q-ml-xs">{{ equipment.name }}</div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Codigo serial:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.serial_number }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Inventario UMAG:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.umag_inventory_code }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Marca:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.brand_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Modelo:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.model_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Número de modelo:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.model_number }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Periodo de mantención:
              </div>
              <div
                v-if="equipment.maintenance_period == null"
                class="col field-content q-ml-xs"
              >
                No aplica
              </div>
              <div v-else class="col field-content q-ml-xs">
                Cada {{ equipment.maintenance_period }} meses
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Observación:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.observation }}
              </div>
            </div>
          </q-card-section>
        </q-card-section>
        <q-separator horizontal />
        <q-card-section horizontal class="row">
          <q-card-section class="col-4">
            <div class="text-h5 q-mb-md text-center">
              Datos Ubicación<q-btn
                class="q-ml-md glossy"
                icon="edit"
                color="positive"
                @click="editLocation"
              />
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Sala:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.room_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Unidad:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.unit_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Edificio:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.building_name }}
              </div>
            </div>
          </q-card-section>
          <q-separator />
          <!--Datos compra-->
          <q-card-section class="col">
            <div class="text-h5 q-mb-md text-center">
              Datos compra<q-btn
                class="q-ml-md glossy"
                icon="edit"
                color="positive"
                @click="editPurchase"
              />
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Proveedor:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.supplier_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Fecha de recepción:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.reception_date }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Número factura:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.invoice_number }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Proyecto:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.project_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Etapa:</div>
              <div class="col field-content q-ml-xs">
                {{ equipment.stage_name }}
              </div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">
                Dueño proyecto:
              </div>
              <div class="col field-content q-ml-xs">
                {{ equipment.project_owner_name }}
              </div>
            </div>
          </q-card-section>
        </q-card-section>
      </q-card>
      <div
        v-if="equipment.maintenance_period != null"
        class="q-mt-md maintenance-table"
      >
        <NoRedirectTable
          title="Mantenimientos"
          :columns="columns_maintenances"
          :rows="maintenances"
          :addFunction="addFunction"
          :deleteFunction="removeMaintenance"
          :editFunction="editMaintenance"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import Carousel from "src/components/Carousel.vue";
import NoRedirectTable from "src/components/NoRedirectTable.vue";
import FormModal from "src/components/FormModal.vue";
import EditEquipmentProduct from "./EditEquipmentProduct.vue";
import EditEquipmentLocation from "./EditEquipmentLocation.vue";
import EditEquipmentPurchase from "./EditEquipmentPurchase.vue";
import EditMaintenance from "./EditMaintenance.vue";
import { useQuasar } from "quasar";
import { columns_maintenances } from "src/constants/columns.js";
import { sendRequest } from "src/axios/instance.js";

const $q = useQuasar();

const content_loaded = ref(false);

const img_api = ref(null);
const equipment = ref({});
const maintenances = ref([]);
const last_maintenance = ref({});
const project = ref(null);

const api_prefix = process.env.API_URL;

const route = useRoute();
const router = useRouter();
const id = computed(() => route.params.id);
const query_equipment = api_prefix + "/equipments/" + id.value;
const query_maintenances = api_prefix + "/maintenances/" + id.value;
const query_last_maintenance =
  api_prefix + "/maintenances/last_maintenance/" + id.value;

function padTo2Digits(num) {
  return num.toString().padStart(2, "0");
}

function formatDate(date) {
  return [
    date.getFullYear(),
    padTo2Digits(date.getMonth() + 1),
    padTo2Digits(date.getDate()),
  ].join("-");
}

function createNextMaintenance() {
  const dateString = last_maintenance.value.date + "T00:00:00";
  const months = equipment.value.maintenance_period;
  let date = new Date(dateString);
  date.setDate(date.getDate() + months * 30);
  date = formatDate(date);
  const data = {
    id: null,
    date: date,
    observations: "Próxima mantención programada",
    state: null,
    maintenance_type: "Programada",
    equiptment_id: equipment.value.id,
  };
  maintenances.value.unshift(data);
  maintenances.value.sort((x, y) => {
    const date1 = new Date(x.date + "T00:00:00");
    const date2 = new Date(y.date + "T00:00:00");
    if (date1 < date2) {
      return -1;
    }
    return 1;
  });
}

async function getEquipment() {
  try {
    const response = await sendRequest({
      method: "GET",
      url: query_equipment,
    });
    equipment.value = response.data;
    img_api.value = api_prefix + "/equipments/image/" + equipment.value.id;
    getMaintenances();
  } catch (error) {}
}

async function getMaintenances() {
  try {
    const response = await sendRequest({
      method: "GET",
      url: query_maintenances,
    });
    maintenances.value = response.data;
    getLastMaintenance();
  } catch (error) {}
}

async function getLastMaintenance() {
  try {
    const response = await sendRequest({
      method: "GET",
      url: query_last_maintenance,
    });
    last_maintenance.value = response.data;
    createNextMaintenance();
  } catch (error) {}
}

function addFunction() {
  $q.dialog({
    component: FormModal,
    componentProps: {
      title: "Agregar mantenimiento",
      fields: [
        {
          label: "Fecha",
          type: "date",
          defaultvalue: null,
          rules: [(val) => (val && val != null) || "Este campo es obligatorio"],
        },
        {
          label: "Tipo de mantenimiento",
          type: "select",
          defaultvalue: null,
          options: [
            { id: "Programada", name: "Programada" },
            { id: "Correctiva", name: "Correctiva" },
          ],
          option_value: "id",
          option_label: "name",
          not_found_label: "No hay tipos de mantenimiento",
          rules: [(val) => (val && val != null) || "Este campo es obligatorio"],
        },
        {
          label: "Estado",
          type: "select",
          defaultvalue: null,
          options: [
            { id: "0", name: "Sin realizar" },
            { id: "1", name: "Realizado" },
          ],
          option_value: "id",
          option_label: "name",
          not_found_label: " ",
          rules: [(val) => (val && val != null) || "Este campo es obligatorio"],
        },
        {
          label: "Observaciones",
          type: "text",
          defaultvalue: null,
          autogrow: true,
          rules: [(val) => (val && val != null) || "Este campo es obligatorio"],
        },
      ],
    },
  })
    .onOk(async (data) => {
      const state = data[2] == 1 ? true : data[2] == 0 ? false : null;
      const maintenance_data = {
        date: data[0],
        observations: data[3],
        maintenance_type: data[1],
        state: state,
        equiptment_id: equipment.value.id,
      };

      try {
        const response = await sendRequest({
          method: "POST",
          url: api_prefix + "/maintenances",
          data: maintenance_data,
        });
        getMaintenances();
      } catch (error) {}
    })
    .onCancel(() => {});
}

function editProduct() {
  $q.dialog({
    component: EditEquipmentProduct,
    componentProps: {
      id: equipment.value.id,
      name_value: equipment.value.name,
      serial_number_value: equipment.value.serial_number,
      umag_inventory_code_value: equipment.value.umag_inventory_code,
      brand_value: {
        id: equipment.value.brand_id,
        name: equipment.value.brand_name,
      },
      model_value: {
        id: equipment.value.model_id,
        name: equipment.value.model_name,
      },
      model_number_value: {
        id: equipment.value.model_number_id,
        name: equipment.value.model_number,
      },
      maintenance_period_value: equipment.value.maintenance_period,
      observation_value: equipment.value.observation,
    },
  }).onOk((data) => {});
}

function editLocation() {
  $q.dialog({
    component: EditEquipmentLocation,
    componentProps: {
      id: equipment.value.id,
      room_value: {
        id: equipment.value.room_id,
        name: equipment.value.room_name,
      },
      unit_value: {
        id: equipment.value.unit_id,
        name: equipment.value.unit_name,
      },
      building_value: {
        id: equipment.value.building_id,
        name: equipment.value.building_name,
      },
    },
  }).onOk((data) => {});
}

function editPurchase() {
  const projectData = {
    project_id: project.value ? project.value.id : null,
    project_name: project.value ? project.value.project_name : null,
    stage_id: project.value ? project.value.stage_id : null,
    stage_name: project.value ? project.value.stage_name : null,
  };
  $q.dialog({
    component: EditEquipmentPurchase,
    componentProps: {
      id: equipment.value.id,
      supplier_value: {
        id: equipment.value.supplier_id,
        name: equipment.value.supplier_name,
      },
      reception_date_value: equipment.value.reception_date,
      invoice_value: {
        id: equipment.value.invoice_id,
        name: equipment.value.invoice_number,
      },
      project_value: {
        id: equipment.value.project_id,
        name: equipment.value.project_name,
      },
      stage_value: {
        id: equipment.value.stage_id,
        name: equipment.value.stage_name,
      },
    },
  }).onOk((data) => {});
}

function editMaintenance(maintenance) {
  $q.dialog({
    component: EditMaintenance,
    componentProps: {
      id: maintenance.id,
      date_value: maintenance.date,
      type_value: {
        id: maintenance.maintenance_type,
        name: maintenance.maintenance_type,
      },
      typeOptions: [
        { id: "Programada", name: "Programada" },
        { id: "Correctiva", name: "Correctiva" },
      ],
      state_value: {
        id: maintenance.state ? 1 : 0,
        name: maintenance.state ? "Realizado" : "Sin realizar",
      },
      stateOptions: [
        { id: "0", name: "Sin realizar" },
        { id: "1", name: "Realizado" },
      ],
      observation_value: maintenance.observations,
      equiptment_id: maintenance.equiptment_id,
    },
  }).onOk(() => {
    getMaintenances();
  });
}

function removeMaintenance(maintenance) {
  $q.dialog({
    title: "Eliminar mantenimiento",
    message: "Se eliminara el mantenimiento",
    ok: {
      color: "negative",
      label: "Aceptar y eliminar",
    },
    cancel: {
      color: "warning",
      label: "Cancelar y mantener",
    },
  })
    .onOk(async () => {
      const maintenance_id = maintenance.id;
      try {
        const response = await sendRequest({
          method: "DELETE",
          url: api_prefix + "/maintenances/" + maintenance_id,
        });
        getMaintenances();
      } catch (error) {
        if (error.response.status === 403) {
          router.push({ path: "/login" });
        }
      }
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    });
}

onMounted(() => {
  getEquipment();
  content_loaded.value = true;
});
</script>

<style scoped>
.my-card {
  width: 100%;
}

.maintenance-table {
  width: 100%;
}
.field-label {
  font-size: 16px;
  font-weight: bold;
}

.field-content {
  font-size: 16px;
  font-weight: 500;
}

.q-page {
  color: #262626;
}
</style>
