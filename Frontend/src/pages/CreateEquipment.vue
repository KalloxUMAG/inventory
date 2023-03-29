<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form @submit.prevent="onSubmit" @reset="onReset" class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pt-xl relative-position" ref="createEquipmentForm">

        <!--Datos Producto-->

        <q-input filled v-model="name" maxlength="49" label="Nombre del equipo" lazy-rules
        :rules="[
          val => val && val.length > 0 || 'Este campo es obligatorio',
          val => val && val.length < 50 || 'El nombre debe contener menos de 50 caracteres'
        ]"/>
        <q-input filled v-model="serial" maxlength="30" label="Código serial" lazy-rules
          :rules="[
            val => val && val.length > 0 || 'Este campo es obligatorio',
            val => val && val.length < 256 || 'Máximo 255 caracteres'
          ]"/>
        <q-input filled v-model="inventory" maxlength="11" type="number" label="Inventario UMAG" lazy-rules :rules="[val => val.length < 26 && val >0 || 'El valor debe ser mayor que 0 y tener un maximo de 25 dígitos']"/>
        <!--Modelo-->
        <div v-if="!this.newmodelstate">
          <SelectForm :options="modelOptions" option_value="id" option_label="name" label="Modelo" not_found_label="No hay modelos disponibles" @updateModel="(value) => model = value"/>
          <div class="row justify-end q-mt-md">
            <q-btn label="Añadir modelo" icon="add" class="bg-green-3 text-caption" @click="this.newmodelstate = !this.newmodelstate"/>
          </div>
        </div>

        <div v-else>
          <div class="row q-col-gutter-md">
            <q-input class="col" label="Marca" v-model="newbrand" lazy-rules/>
            <q-input class="col" label="Modelo" v-model="newmodel" lazy-rules/>
            <q-input class="col" label="Número de Producto" type="number" v-model="newnumber" lazy-rules/>
          </div>
          <div class="row justify-end q-pt-sm q-pb-md">
            <q-btn label="Cancelar" color="negative" class="q-ml-sm" @click="this.newmodelstate = !this.newmodelstate"/>
          </div>
        </div>

        <q-input filled v-model="maintenance" type="number" label="Periodo de mantención (días)" lazy-rules/>
        <q-input filled v-model="observation" type="textarea" label="Observación" lazy-rules/>

        <!--Datos de compra-->
        <div v-if="!this.newsupplierstate">
          <SelectForm :options="suppliersOptions" option_value="id" option_label="name" label="Proveedor" not_found_label="No hay proveedores disponibles" @updateModel="(value) => supplier = value"/>
          <div class="row justify-end q-mt-md">
            <q-btn label="Añadir proveedor" icon="add" class="bg-green-3 text-caption" @click="this.newsupplierstate = !this.newsupplierstate"/>
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input v-model="newsuppliername" label="Nombre proveedor" class="col"/>
            <q-input v-model="newsupplierrut" label="Rut" class="col q-ml-md"/>
            <q-input v-model="newsupplieraddress" label="Dirección" class="col q-ml-md"/>
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn label="Cancelar" color="negative" @click="this.newsupplierstate = !this.newsupplierstate"/>
          </div>
        </div>

        <q-input filled v-model="reception_date" type="date" label="Fecha de recepción"  stack-label lazy-rules
          :rules="[val => val && val != null || 'Este campo es obligatorio']"/>

        <!--Invoices-->
        <div v-if="!this.newinvoicestate">
          <SelectForm :options="invoicesOptions" option_value="id" option_label="number" label="Facturas" not_found_label="No hay facturas disponibles" @updateModel="(value) => invoice = value"/>
          <div class="row justify-end q-mt-md">
            <q-btn label="Añadir factura" icon="add" class="bg-green-3 text-caption" @click="this.newinvoicestate = !this.newinvoicestate"/>
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input v-model="newinvoicenumber" label="Numero" type="number" class="col"/>
            <q-input v-model="newinvoicedate" label="Fecha" type="date" stack-label class="col q-ml-md"/>
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn label="Cancelar" color="negative" @click="this.newinvoicestate = !this.newinvoicestate"/>
          </div>
        </div>

        <!--Projects and stages-->

        <div class="row justify-center">
          <div v-if="!this.newprojectstate" class="col q-mr-md">
            <SelectForm class="row q-mr-md" :options="projectOptions" option_value="id" option_label="name" label="Proyectos" not_found_label="No hay proyectos disponibles" @updateModel="(value) => {project = value; getStages()}"/>
            <div class="row justify-end q-pt-md">
              <q-btn label="Añadir Proyecto" icon="add" class="bg-green-3 text-caption q-mr-md" @click="this.newprojectstate = !this.newprojectstate"/>
            </div>
          </div>
          <div v-else class="col-8 q-mr-lg">
            <div class="row">
              <q-input v-model="newprojectname" label="Nombre proyeto" class="col"/>
              <q-input v-model="newprojectdate" label="Fecha" type="date" stack-label class="col-3 q-ml-md"/>
            </div>
            <div class="row justify-end q-mt-sm">
              <q-btn label="Cancelar" color="negative" @click="this.newprojectstate = !this.newprojectstate"/>
            </div>
          </div>

          <div v-if="!this.newstagestate && !this.newprojectstate" class="col q-ml-md">
            <SelectForm class="row" :options="stagesOptions" option_value="id" option_label="name" label="Etapas" not_found_label="No hay etapas disponibles" @updateModel="(value) => stage = value"/>
            <div class="row justify-end q-pt-md">
              <q-btn label="Añadir Etapa" icon="add" class="bg-green-3 text-caption q-ml-md" @click="this.newstagestate = !this.newstagestate"/>
            </div>
          </div>
          <div v-else class="col">
            <div class="row">
              <q-input v-model="newstagename" label="Nombre etapa" class="col"/>
            </div>
            <div v-if="this.newstagestate && !this.newprojectstate" class="row justify-end q-mt-sm">
              <q-btn label="Cancelar" color="negative" @click="this.newstagestate = !this.newstagestate"/>
            </div>
          </div>
        </div>


        <!--Location-->
        <div class="row justify-center">
          <div v-if="!this.newbuildingstate" class="col q-mr-md">
            <SelectForm class="row q-mr-md" :options="buildingOptions" option_value="id" option_label="name" label="Edificio" not_found_label="No hay edificios disponibles" @updateModel="(value) => {building = value; getUnits()}"/>
            <div class="row justify-end q-pt-md">
              <q-btn label="Añadir Edificio" icon="add" class="bg-green-3 text-caption q-mr-md" @click="this.newbuildingstate = !this.newbuildingstate"/>
            </div>
          </div>
          <div v-else class="col">
            <div class="row">
              <q-input v-model="newbuildingname" label="Nombre edificio" class="col"/>
            </div>
            <div class="row justify-end q-mt-sm">
              <q-btn label="Cancelar" color="negative" @click="this.newbuildingstate = !this.newbuildingstate"/>
            </div>
          </div>
          <div v-if="!this.newbuildingstate && !this.newunitstate" class="col q-mr-md">
            <SelectForm class="row q-mr-md" :options="unitOptions" option_value="id" option_label="name" label="Unidad" not_found_label="No hay una unidad disponible" @updateModel="(value) => {unit = value; getRooms()}"/>
            <div class="row justify-end q-pt-md">
              <q-btn label="Añadir unidad" icon="add" class="bg-green-3 text-caption q-mr-md" @click="this.newunitstate = !this.newunitstate"/>
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input v-model="newunitname" label="Nombre unidad" class="col"/>
            </div>
            <div v-if="!this.newbuildingstate && this.newunitstate" class="row justify-end q-mt-sm">
              <q-btn label="Cancelar" color="negative" @click="this.newunitstate = !this.newunitstate"/>
            </div>
          </div>
          <div v-if="!this.newbuildingstate && !this.newunitstate && !this.newroomstate" class="col q-mr-md">
            <SelectForm class="row q-mr-md" :options="roomOptions" option_value="id" option_label="name" label="Sala" not_found_label="No hay salas disponibles" @updateModel="(value) => {room = value}"/>
            <div class="row justify-end q-pt-md">
              <q-btn label="Añadir sala" icon="add" class="bg-green-3 text-caption q-mr-md" @click="this.newroomstate = !this.newroomstate"/>
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input v-model="newroomname" label="Nombre sala" class="col"/>
            </div>
            <div v-if="!this.newbuildingstate && !this.newunitstate && this.newroomstate" class="row justify-end q-mt-sm">
              <q-btn label="Cancelar" color="negative" @click="this.newroomstate = !this.newroomstate"/>
            </div>
          </div>
        </div>


        <div class="row justify-end">
          <q-btn label="Submit" type="submit" color="primary"/>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        </div>
        <q-inner-loading :showing="loading" label="Creando equipamiento" label-class="text-deep-orange" label-style="font-size: 1.6em"/>
      </q-form>
    </div>
  </q-page>
</template>

<script>
  import {useQuasar} from 'quasar';
  import {ref} from 'vue';
  import axios from 'axios'
  import SelectForm from 'src/components/SelectForm.vue'

  export default{
    components: {
      SelectForm
    },

    setup(){
      const building = ref(null)
      const buildingOptions = ref([])
      const buildings = ref([])
      const createEquipmentForm = ref(null)
      const name = ref(null)
      const serial = ref(null)
      const inventory = ref(null)
      const invoice = ref(null)
      const invoices = ref([])
      const invoicesOptions = ref([])
      const loading = ref(false)
      const model = ref(null)
      const models = ref([])
      const modelOptions = ref([])
      const maintenance = ref(null)
      const observation = ref(null)
      const newbuildingname = ref(null)
      const newbuildingstate = ref(false)
      const newinvoicestate = ref(false)
      const newmodelstate = ref(null)
      const newmodel = ref(null)
      const newbrand = ref(null)
      const newinvoicenumber = ref(null)
      const newinvoicedate = ref(null)
      const newnumber = ref(null)
      const newprojectstate = ref(null)
      const newprojectname = ref(null)
      const newprojectdate = ref(null)
      const newroomname = ref(null)
      const newroomstate = ref(null)
      const newstagestate = ref(null)
      const newstagename = ref(null)
      const newsupplierstate = ref(false)
      const newsuppliername = ref(null)
      const newsupplierrut = ref(null)
      const newsupplieraddress = ref(null)
      const newunitname = ref(null)
      const newunitstate = ref(false)
      const project = ref(null)
      const projects = ref([])
      const projectOptions = ref([])
      const reception_date = ref(null)
      const stage = ref(null)
      const stages = ref([])
      const stagesOptions = ref([])
      const room = ref(null)
      const rooms = ref([])
      const roomOptions = ref([])
      const supplier = ref(null)
      const suppliers = ref([])
      const suppliersOptions = ref([])
      const unit = ref(null)
      const unitOptions = ref([])
      const units = ref([])
      const $q = useQuasar()

      const getBuildings = () => {
        axios.get("http://localhost:8000/api/buildings").then(
          response => {
            buildings.value = response.data
            buildingOptions.value = buildings.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      }

      const getInvoices = () => {
        axios.get("http://localhost:8000/api/invoices").then(
          response => {
            invoices.value = response.data
            invoicesOptions.value = invoices.value.map(x => {
              return {id: x.id, number: x.number}
            })
          }
        )
      }

      const getModels = () => {
        axios.get("http://localhost:8000/api/models").then(
          response => {
            models.value = response.data
            modelOptions.value = models.value.map(x => {
              return {id: x.id, name: x.brand+" "+x.model+" "+x.product_number}
            })
          }
        )
      }

      const getProjects = () => {
        axios.get("http://localhost:8000/api/projects").then(
          response => {
            projects.value = response.data
            projectOptions.value = projects.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      }

      const getRooms = () => {
        const api_url = "http://localhost:8000/api/rooms/"+unit.value
        axios.get(api_url).then(
          response => {
            room.value = null
            rooms.value = response.data
            roomOptions.value = rooms.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      }

      const getStages = () => {
        const api_url = "http://localhost:8000/api/stages/"+project.value
        axios.get(api_url).then(
          response => {
            stage.value = null
            stages.value = response.data
            stagesOptions.value = stages.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      }

      const getSuppliers = () => {
        axios.get("http://localhost:8000/api/suppliers").then(
          response => {
            suppliers.value = response.data
            suppliersOptions.value = suppliers.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      };

      const getUnits = () => {
        const api_url = "http://localhost:8000/api/units/"+building.value
        axios.get(api_url).then(
          response => {
            unit.value = null
            room.value = null
            roomOptions.value = []
            units.value = response.data
            unitOptions.value = units.value.map(x => {
              return {id: x.id, name: x.name}
            })
          }
        )
      }

      const onReset = () => {
        name.value = null
        serial.value = null
        inventory.value = null
        model.value = null
        maintenance.value = null
        observation.value = null
        reception_date.value = null
      };

      async function createNewBuilding(){
        if (!newbuildingstate.value){
          return building.value
        }

        const buildingdata = {
          'name': newbuildingname.value
        }

        try{
          const response = await axios.post("http://localhost:8000/api/buildings", buildingdata)
          return response.data
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear el edificio: ' + error
          })
        }
      }

      async function createNewInvoice(equipmentdata){
        if (!newinvoicestate.value){
          return equipmentdata;
        }

        const invoicedata = {
          'number': newinvoicenumber.value,
          'date': newinvoicedate.value
        }

        try{
          const response = await axios.post("http://localhost:8000/api/invoices", invoicedata)
          equipmentdata['invoice_id'] = response.data
          return equipmentdata
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear la factura: ' + error
          })
        }
      }

      async function createNewModel(equipmentdata){
        if (!newmodelstate.value){
          return equipmentdata;
        }

        const newmodeldata = {
        'model': newmodel.value,
        'brand': newbrand.value,
        'product_number': newnumber.value
        }

        try{
          const response = await axios.post("http://localhost:8000/api/models", newmodeldata)
          equipmentdata['model_id'] = response.data
          return equipmentdata
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear el modelo: ' + error
          })
        }
      }

      async function createNewProject(relationdata) {
        if (!newprojectstate.value){
          return relationdata;
        }

        const projectname = newprojectname.value

        if(projectname.trim().length == 0){
          return relationdata;
        }

        const projectdata = {
          'name': newprojectname.value,
          'start_date': newprojectdate.value
        }

        try{
          const response = await axios.post("http://localhost:8000/api/projects", projectdata)
          relationdata['project_id'] = response.data
          return relationdata
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear el proyecto: ' + error
          })
        }
      }

      async function createNewUnit(building_id){
        if (!newbuildingstate.value && !newunitstate.value){
          return unit.value
        }

        const unitdata = {
          'name': newunitname.value,
          'building_id': building_id
        }

        try{
          const response = await axios.post("http://localhost:8000/api/units", unitdata)
          return response.data
        }catch(error){
          $q.notify({
              color: 'red-3',
              textColor: 'white',
              icon: 'error',
              message: 'No se pudo crear la unidad: ' + error
            })
        }
      }

      async function createNewRoom(unit_id){
        if (!newbuildingstate.value && !newunitstate.value && !newroomstate.value){

          return room.value
        }
        const roomdata = {
          'name': newroomname.value,
          'unit_id': unit_id
        }

        try{
          const response = await axios.post("http://localhost:8000/api/rooms", roomdata)
          return response.data
        }catch(error){
          $q.notify({
              color: 'red-3',
              textColor: 'white',
              icon: 'error',
              message: 'No se pudo crear la sala: ' + error
            })
        }
      }

      async function createNewSupplier(equipmentdata) {
        if (!newsupplierstate.value){
          return equipmentdata;
        }
        const supplierdata = {
          'name': newsuppliername.value,
          'rut': newsupplierrut.value,
          'city_address': newsupplieraddress.value
        }
        try{
          const response = await axios.post("http://localhost:8000/api/suppliers", supplierdata)
          equipmentdata['supplier_id'] = response.data
          return equipmentdata
        }catch(error){
          $q.notify({
              color: 'red-3',
              textColor: 'white',
              icon: 'error',
              message: 'No se pudo crear el proveedor: ' + error
            })
        }
      }

      async function createNewStage(relationdata){
        if(!newstagestate.value && !newprojectstate.value){
          return relationdata;
        }

        const stagename = newstagename.value

        if(stagename.trim().length == 0){
          return relationdata;
        }

        const stagedata = {
          'name': newstagename.value,
          'project_id': relationdata.project_id
        }

        try{
          const response = await axios.post("http://localhost:8000/api/stages", stagedata)
          relationdata['stage_id'] = response.data
          return relationdata
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear la etapa: ' + error
          })
        }
      }

      async function createNewEquipment (equipmentdata) {
        try{
          const response = await axios.post("http://localhost:8000/api/equipments", equipmentdata)
          if(response.status == 201){
            $q.notify({
              color: 'green-4',
              textColor: 'white',
              icon: 'check',
              message: 'Equipo creado con éxito'
            })
          }
          return response.data
        }catch(error){
          $q.notify({
            color: 'red-3',
            textColor: 'white',
            icon: 'error',
            message: 'No se pudo crear el equipo: ' + error
          })
        }
      }

      async function createNewProjectEquipment (equipment_id) {
        let relationdata = {
          'equipment_id': equipment_id,
          'project_id': project.value,
          'stage_id': stage.value
        }

        relationdata = await createNewProject(relationdata)
        relationdata = await createNewStage(relationdata)

        try{
          const response = await axios.post("http://localhost:8000/api/equipments_projects", relationdata)

          if(response.status == 201){
              $q.notify({
                color: 'green-4',
                textColor: 'white',
                icon: 'check',
                message: 'Relación creada con éxito'
              })
            }
        }catch(error){
          $q.notify({
              color: 'red-3',
              textColor: 'white',
              icon: 'error',
              message: 'No se pudo crear la relacion: ' + error
            })

        }

      }

      async function onSubmit() {
        createEquipmentForm.value.resetValidation()
        let equipmentdata = {
          'name': name.value,
          'serial_number': serial.value,
          'umag_inventory_code': inventory.value,
          'reception_date': reception_date.value,
          'maintenance_period': maintenance.value,
          'observation': observation.value,
          'model_id': model.value,
          'supplier_id': supplier.value,
          'invoice_id': invoice.value,
          'room_id': room.value
        }
        loading.value = true
        const building_id = await createNewBuilding()
        const unit_id = await createNewUnit(building_id)
        const room_id = await createNewRoom(unit_id)

        equipmentdata['room_id'] = room_id

        equipmentdata = await createNewModel(equipmentdata)
        equipmentdata = await createNewSupplier(equipmentdata)
        equipmentdata = await createNewInvoice(equipmentdata)

        const equipment_id = await createNewEquipment(equipmentdata)
        await createNewProjectEquipment(equipment_id)
        loading.value = false
        //onReset()

      }

      return{
        building,
        buildingOptions,
        buildings,
        createEquipmentForm,
        name,
        serial,
        inventory,
        invoice,
        invoices,
        invoicesOptions,
        loading,
        model,
        maintenance,
        observation,
        modelOptions,
        newbuildingname,
        newbuildingstate,
        newinvoicestate,
        newmodelstate,
        newinvoicedate,
        newinvoicenumber,
        newmodel,
        newbrand,
        newnumber,
        newprojectstate,
        newprojectname,
        newprojectdate,
        newroomname,
        newroomstate,
        newstagestate,
        newstagename,
        newsupplierstate,
        newsuppliername,
        newsupplierrut,
        newsupplieraddress,
        newunitname,
        newunitstate,
        room,
        rooms,
        roomOptions,
        project,
        projects,
        projectOptions,
        reception_date,
        stage,
        stages,
        stagesOptions,
        supplier,
        suppliers,
        suppliersOptions,
        unit,
        units,
        unitOptions,
        getBuildings,
        getInvoices,
        getModels,
        getProjects,
        getRooms,
        getStages,
        getSuppliers,
        getUnits,
        onReset,
        onSubmit,
      }
    },

    mounted(){
      this.getInvoices();
      this.getModels();
      this.getProjects();
      this.getSuppliers();
      this.getBuildings();
    },
  }


</script>

<style>
input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}
</style>
