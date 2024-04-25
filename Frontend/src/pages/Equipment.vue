<template>
  <div v-if="equipment != null" class="row justify-center">
    <q-card class="my-card row q-pa-md q-mb-lg justify-between" flat bordered>
      <div class="flex item-title"><q-icon name="biotech" size="24px"/><div class="text-subtitle1 text-bold text-uppercase">  {{ equipment.name  }} - {{ equipment.model_name }}</div></div>
      <q-btn outline color="secondary" label="Editar" class="floar-right" @click="editEquipment"/>
    </q-card>

    <q-card class="my-card row q-pa-md gap-lg" flat bordered>
      <div class="col-12 col-md-7 col-lg-6 container image-visor">
        <Carousel v-if="img_api" :api_endpoint="img_api" />
      </div>

      <div class="col container">
        <InfoSection title="Información general" :fields="[
        {
          label: 'Nombre',
          value: equipment.name
        },
        {
          label: 'Codigo serial',
          value: equipment.serial_number
        },
        {
          label: 'Inventario UMAG',
          value: equipment.umag_inventory_code
        },
        {
          label: 'Marca',
          value: equipment.brand_name
        },
        {
          label: 'Modelo',
          value: equipment.model_name
        },
        {
          label: 'Número de modelo',
          value: equipment.model_number
        },
        {
          label: 'Periodo de mantención',
          value: maintenance_period
        },
        {
          label: 'Observación',
          value: equipment.observation
        }
      ]"/>
      <InfoSection title="Ubicación" :fields="[
        {
          label: 'Edificio',
          value: equipment.building_name
        },
        {
          label: 'Unidad',
          value: equipment.unit_name
        },
        {
          label: 'Sala',
          value: equipment.room_name
        }
      ]"/>
      <InfoSection title="Compra" :fields="[
        {
          label: 'Proveedor',
          value: equipment.supplier_name
        },
        {
          label: 'Fecha de recepción',
          value: equipment.reception_date
        },
        {
          label: 'Factura',
          value: equipment.invoice_number
        },
        {
          label: 'Proyecto',
          value: project ? project.project_name : null
        },
        {
          label: 'Etapa',
          value: project ? project.stage_name : null
        }
      ]"/>
      </div>
    </q-card>
    <div
      v-if="equipment.maintenance_period === null"
      class="q-mt-md maintenance-table"
    >
      <q-card class="no-shadow bg-transparent" >
        <q-card-section class="q-pl-none col-12">
          <div class="text-subtitle1 q-pl-md space-between">
            Lista de Mantenimientos
            <div class="actions-buttons">
              <q-input
                outlined
                bg-color="white"
                dense
                debounce="300"
                placeholder="Buscar"
                v-model="filter"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
              <q-btn
                class="add-btn q-mr-sm"
                @click="addFunction"
                icon="add"
                label="Agregar"
                flat
              />
            </div>
          </div>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <q-table
            row-key="id"
            :columns="columns_maintenances"
            :rows="maintenances"
            no-data-label="No hay registros para mostrar"
            rows-per-page-label="Registros por pagina"
            flat
            bordered
            no-wrap
            :filter="filter"
            class="card-style"
          >
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                  :class="['text-italic', 'table-header']"
                >
                  {{ col.label }}
                </q-th>
              </q-tr>
            </template>
            <template v-slot:body-cell="props">
              <q-td
                :props="props"
              >
                {{ props.value }}
              </q-td>
            </template>
            <template v-slot:body-cell-state="props">
              <q-td
                :props="props"
              >
              <q-icon
                v-if="props.row.state == true"
                size="md"
                name="done_all"
                color="positive"
                ><q-tooltip>Realizado</q-tooltip></q-icon
              >
              <q-icon
                v-if="props.row.state == false"
                size="md"
                name="close"
                color="negative"
                ><q-tooltip>No realizado</q-tooltip></q-icon
              >
              <q-icon
                v-if="props.row.state == null"
                size="md"
                name="play_arrow"
                color="warning"
                ><q-tooltip>Próximo</q-tooltip></q-icon
              >
              </q-td>
            </template>
            <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  dense
                  icon="edit"
                  color="warning"
                  @click="editMaintenance(props.row)"
                />
                <q-btn
                  v-if="props.row.id != null"
                  flat
                  dense
                  icon="delete"
                  color="negative"
                  @click="removeMaintenance(props.row)"
                />
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>
  </div>
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
import InfoSection from "src/components/item-page/InfoSection.vue";

const $q = useQuasar();

const content_loaded = ref(false);
const filter = ref("");
const img_api = ref(null);
const equipment = ref({});
const maintenances = ref([]);
const last_maintenance = ref({});
const project = ref(null);
const maintenance_period = ref(null);

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
    maintenance_period.value = equipment.value.maintenance_period ? "Cada " + equipment.value.maintenance_period + " meses" : "No aplica";
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

const editEquipment = () => {
  console.log("Edit equipment " + equipment.value.id);
};

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
.item-title{
  align-content: center;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}

.container{
  border: 1px solid #d1d1d1 !important;
  border-radius: 12px !important;
  padding: 8px;
  overflow: visible;
}

.gap-lg{
  gap: 24px;
}

.image-visor{
  border: none !important;
  max-height: 500px;
  padding: 0;
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

.card-style{
  border-radius: 12px;
}
.space-between{
  display: flex;
  justify-content: space-between;
}
.actions-buttons{
  display: inline-flex;
  gap: 10px;
  .add-btn{
    background-color: var(--add-btn-bg-color);
    color: var(--add-btn-text-color);
  }
}
</style>
