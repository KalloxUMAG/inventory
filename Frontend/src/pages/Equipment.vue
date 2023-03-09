<template>
    <q-page padding>
      <div v-if="this.equipment != null" class="row justify-center bg-secondary">
        <q-card class="my-card" flat bordered>
          <q-item>
           <div class="text-h5">{{ this.equipment.name }} - {{ this.equipment.serial_number }}</div>
          </q-item>
          <q-separator/>
          <q-card-section>
            <div class="col-4">
              <div class="row">Nombre: {{ this.equipment.name }}</div>
              <div class="row">Codigo producto: {{ this.equipment.serial_number }}</div>
              <div class="row">Inventario UMAG: {{ this.equipment.umag_inventory_code }}</div>
              <div class="row">Proveedor: {{ this.equipment.supplier_name }}</div>
              <div class="row">Modelo: {{ this.equipment.model_model }}</div>
              <div class="row">Factura: {{ this.equipment.invoice_number }}</div>
            </div>
          </q-card-section>
          <q-card-section>
            <div class="text-h6">Codigo</div>
          </q-card-section>
        </q-card>

        <div class="col-4">
          <div class="row">Ubicacion: {{ this.equipment.building_name }}/{{ this.equipment.unit_name }}/{{ this.equipment.room_name }}</div>
          <div class="row">Descripcion</div>
          <div class="row">{{ this.equipment.observation }}</div>
        </div>
      </div>
      <h3>Equipamiento</h3>
      <pre>{{ this.equipment }}</pre>
      <pre>{{ this.maintenances }}</pre>
      <pre>{{ this.projects }}</pre>
  </q-page>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import {computed} from 'vue'
import axios from 'axios'

export default {
  data(){
    return{
      equipment: null,
      maintenances: null,
      projects: null
    }
  },
  methods:{
    getEquipment(){
      axios.get(this.query_equipment).then(
        response => (
          this.equipment = response.data
        )
      )
    },
    getMaintenances(){
      axios.get(this.query_maintenances).then(
        response => (
          this.maintenances = response.data
        )
      )
    },
    getProjects(){
      axios.get(this.query_projects).then(
        response => (
          this.projects = response.data
        )
      )
    },
  },
  mounted(){
    this.getEquipment();
    this.getMaintenances();
    this.getProjects();
  },
  setup() {
    const route = useRoute()
    const id = computed( () => route.params.id)
    const query_equipment = "http://localhost:8000/api/equipments/"+id.value
    const query_maintenances = "http://localhost:8000/api/maintenances/"+id.value
    const query_projects = "http://localhost:8000/api/equipment_projects/"+id.value

    return{
      id,
      query_equipment,
      query_maintenances,
      query_projects
    }
  },
};
</script>


<style scoped>
  .my-card{
    width: 100%;
  }
</style>
