<template>
    <q-page padding>
      <div v-if="this.equipment != null" class="row justify-center bg-secondary">
        <q-card class="my-card" flat bordered>
          <q-item class="row justify-center">
           <div class="text-h5">{{ this.equipment.name }} - {{ this.equipment.serial_number }}</div>
          </q-item>
          <q-separator/>
          <q-card-section horizontal>
            <!--Datos carrucel-->
            <q-card-section class="col-4">
              <Carousel v-if="this.equipment != null" :api_endpoint="img_api"/>
            </q-card-section>
            <q-separator vertical/>
            <!--Datos producto-->
            <q-card-section class="col">
              <div class="text-h5 q-mb-md text-center">Datos producto</div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Nombre:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.name }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Codigo serial:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.serial_number }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Inventario UMAG:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.umag_inventory_code }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Marca:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.brand_name }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Modelo:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.model_name }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Número de modelo:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.model_number }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Periodo de mantención:</div>
                <div v-if="this.equipment.maintenance_period == null" class="col field-content q-ml-xs">No aplica</div>
                <div v-else class="col field-content q-ml-xs">Cada {{ this.equipment.maintenance_period }} meses</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Observación:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.observation }}</div>
              </div>
            </q-card-section>
        </q-card-section>
        <q-separator horizontal/>
        <q-card-section horizontal class="row">
          <q-card-section class="col-4">
            <div class="text-h5 q-mb-md text-center">Datos Ubicación</div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Sala:</div>
              <div class="col field-content q-ml-xs">{{ this.equipment.room_name }}</div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Unidad:</div>
              <div class="col field-content q-ml-xs">{{ this.equipment.unit_name }}</div>
            </div>
            <div class="row q-mb-xs">
              <div class="col-5 field-label text-right q-mr-md">Edificio:</div>
              <div class="col field-content q-ml-xs">{{ this.equipment.building_name }}</div>
            </div>
          </q-card-section>
          <q-separator/>
          <!--Datos compra-->
          <q-card-section class="col">
              <div class="text-h5 q-mb-md text-center">Datos compra</div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Proveedor:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.supplier_name}}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Fecha de recepción:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.reception_date }}</div></div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Número factura:</div>
                <div class="col field-content q-ml-xs">{{ this.equipment.invoice_number }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Proyecto:</div>
                <div class="col field-content q-ml-xs" v-if="this.project != null">{{ this.project.project_name }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Etapa:</div>
                <div class="col field-content q-ml-xs" v-if="this.project != null">{{ this.project.stage_name }}</div>
              </div>
              <div class="row q-mb-xs">
                <div class="col-5 field-label text-right q-mr-md">Patrocinador:</div>
                <div class="col field-content q-ml-xs" v-if="this.project != null && this.project.project_owner != null">{{ this.project.project_owner }}</div>
                <div class="col field-content q-ml-xs" v-else>{{ Ninguno }}</div>
              </div>
            </q-card-section>
        </q-card-section>
        </q-card>
      </div>
      <!--Datos imagen-->
      <div class="row">
        <div class="col-6">

        </div>
      </div>
  </q-page>
</template>

<script>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import axios from 'axios';
import Carousel from "src/components/Carousel.vue"

const columns_maintenances = [
  {
    name: "date",
    align: "left",
    label: "Fecha",
    field: "date",
    sortable: true,
  },
  {
    name: "maintenance_type",
    align: "left",
    label: "Tipo mantenimiento",
    field: "maintenance_type",
    sortable: true,
  },
  {
    name: "observations",
    align: "left",
    label: "Observaciones",
    field: "observations",
    sortable: false,
  },
]

const columns_projects = [
  {
    name: "project_name",
    align: "left",
    label: "Proyecto",
    field: "project_name",
    sortable: true,
  },
  {
    name: "stage_name",
    align: "left",
    label: "Etapa",
    field: "stage_name",
    sortable: false,
  },
  {
    name: "details",
    align: "left",
    label: "Ver detalles",
    field: "details",
    sortable: false,
  },
]

const content_loaded = false

export default {
  components: {
    Carousel,
  },
  data(){
    return{
      img_api: null,
      equipment: null,
      maintenances: null,
      project: null,
    }
  },
  methods:{
    getEquipment(){
      axios.get(this.query_equipment).then(
        response => {
          this.equipment = response.data
          this.img_api = "http://localhost:8000/api/equipments/image/"+this.equipment.id
        }
      )
    },
    getMaintenances(){
      axios.get(this.query_maintenances).then(
        response => {
          this.maintenances = response.data
        }
      )
    },
    getProjects(){
      axios.get(this.query_projects).then(
        response => (
          this.project = response.data
        )
      )
    },
  },
  mounted(){
    this.getEquipment();
    this.getMaintenances();
    this.getProjects();
    this.content_loaded = true
  },
  setup() {
    const route = useRoute()
    const id = computed( () => route.params.id)
    const query_equipment = "http://localhost:8000/api/equipments/"+id.value
    const query_maintenances = "http://localhost:8000/api/maintenances/"+id.value
    const query_projects = "http://localhost:8000/api/equipment_projects/"+id.value

    return{
      content_loaded,
      columns_maintenances,
      columns_projects,
      id,
      query_equipment,
      query_maintenances,
      query_projects,
    }
  },
};
</script>


<style scoped>
  .my-card{
    width: 100%;
  }
  .field-label{
    font-size: 16px;
    font-weight: bold;
  }

  .field-content{
    font-size: 16px;
    font-weight: 500;
  }

  .q-page{
    background-color: #ffe6e9;
    color: #262626;
  }
</style>
