<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form @submit.prevent="onSubmit" @reset="onReset" class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pt-xl" ref="createEquipmentForm">

        <!--Datos Producto-->

        <q-input filled v-model="name" maxlength="49" label="Nombre del equipo" lazy-rules
        :rules="[
          val => val && val.length > 0 || 'Este campo es obligatorio',
          val => val && val.length < 50 || 'El nombre debe contener menos de 50 caracteres'
        ]"/>
        <q-input filled v-model="serial" maxlength="30" label="Código serial" lazy-rules
          :rules="[
            val => val && val.length > 0 || 'Este campo es obligatorio',
            val => val && val.length < 31 || 'Máximo 30 caracteres'
          ]"/>
        <q-input filled v-model="inventory" maxlength="9" type="number" label="Inventario UMAG" lazy-rules :rules="[val => val < 999999999 && val >0 || 'El valor debe estar entre 1 y 999999999']"/>
        <!--Modelo-->
        <q-select v-if="!this.newmodelstate" filled v-model="model" :options="modelOptions" option-value="id" option-label="name" emit-value map-options label="Modelo">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-italic text-grey">
                No hay modelos disponibles
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <div v-if="!this.newmodelstate" class="row justify-end">
          <q-btn label="Añadir modelo" icon="add" class="bg-green-3 text-caption" @click="this.newmodelstate = !this.newmodelstate"/>
        </div>
        <div v-else>
          <q-form @submit="submitModel" @reset="resetModel">
            <div class="row q-col-gutter-md">
              <q-input class="col" label="Marca" v-model="newbrand" lazy-rules/>
              <q-input class="col" label="Modelo" v-model="newmodel" lazy-rules/>
              <q-input class="col" label="Número de Producto" type="number" v-model="newnumber" lazy-rules/>
            </div>
            <div class="row justify-end q-pt-sm q-pb-md">
              <q-btn label="Crear" type="submit" color="primary"/>
              <q-btn label="Cancelar" type="reset" color="negative" class="q-ml-sm" @click="this.newmodelstate = !this.newmodelstate"/>
            </div>
          </q-form>
        </div>

        <q-input filled v-model="maintenance" type="number" label="Periodo de mantención (días)" lazy-rules/>
        <q-input filled v-model="observation" type="textarea" label="Observación" lazy-rules/>

        <!--Datos de compra-->

        <!--Suppliers-->
        <q-select v-if="!this.newsupplierstate" filled v-model="supplier" :options="suppliersOptions" option-value="id" option-label="name" emit-value map-options label="Proveedor">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-italic text-grey">
                No hay proveedores disponibles
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <div v-if="!this.newsupplierstate" class="row justify-end">
          <q-btn v-if="!this.newsupplierstate" label="Añadir proveedor" icon="add" class="bg-green-3 text-caption" @click="this.newsupplierstate = !this.newsupplierstate"/>
        </div>
        <div v-else>
          <div class="row">
            <q-input v-model="newsuppliername" label="Nombre proveedor" class="col"/>
            <q-input v-model="newsupplierrut" label="Rut" class="col q-ml-md"/>
            <q-input v-model="newsupplieraddress" label="Dirección" class="col q-ml-md"/>
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn label="Cancelar" @click="this.newsupplierstate = !this.newsupplierstate"/>
          </div>
        </div>



        <q-input filled v-model="reception_date" type="date" label="Fecha de recepción"  stack-label lazy-rules
          :rules="[val => val && val != null || 'Este campo es obligatorio']"/>

        <!--Invoices-->

        <!--Projects and stages-->

        <!--Location-->



      <div class="row justify-end">
        <q-btn label="Submit" type="submit" color="primary"/>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>
  import {useQuasar} from 'quasar';
  import {ref} from 'vue';
  import axios from 'axios'

  export default{
    setup(){
      const createEquipmentForm = ref(null)
      const name = ref(null)
      const serial = ref(null)
      const inventory = ref(null)
      const model = ref(null)
      const models = ref([])
      const maintenance = ref(null)
      const observation = ref(null)
      const modelOptions = ref([])
      const newmodelstate = ref(null)
      const newmodel = ref(null)
      const newbrand = ref(null)
      const newnumber = ref(null)
      const newsupplierstate = ref(false)
      const newsuppliername = ref(null)
      const newsupplierrut = ref(null)
      const newsupplieraddress = ref(null)
      const reception_date = ref(null)
      const supplier = ref(null)
      const suppliers = ref([])
      const suppliersOptions = ref([])
      const $q = useQuasar()

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

      const getSuppliers = () => {
        axios.get("http://localhost:8000/api/suppliers").then(
          response => {
            suppliers.value = response.data
            suppliersOptions.value = suppliers.value.map(x => {
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

      const onSubmit = () => {
        createEquipmentForm.value.resetValidation()
        const equipmentdata = {
          'name': name.value,
          'serial_number': serial.value,
          'umag_inventory_code': inventory.value,
          'reception_date': reception_date.value,
          'maintenance_period': maintenance.value,
          'observation': observation.value,
          'model_id': model.value
        }

        if (newsupplierstate.value){
          console.log("Deberia agregar al proveedor")
          //Verificar si existe proveedor
          const supplierdata = {
            'name': newsuppliername.value,
            'rut': newsupplierrut.value,
            'city_address': newsupplieraddress.value
          }
          axios.post("http://localhost:8000/api/suppliers", supplierdata).then(
          response => {
            if(response.status == 201){
              $q.notify({
                color: 'green-4',
                textColor: 'white',
                icon: 'check',
                message: 'Proveedor creado con éxito'
              })
              console.log(response.data)
            }
          }, (error) => {

            console.log(error);
          }
        )
        }

        if (newmodelstate.value){
          console.log("Deberia agregar el modelo")
        }

        /*
        axios.post("http://localhost:8000/api/equipments", equipmentdata).then(
          response => {
            if(response.status == 201){
              $q.notify({
                color: 'green-4',
                textColor: 'white',
                icon: 'check',
                message: 'Equipo creado con éxito'
              })
            }
          }, (error) => {

            console.log(error);
          }
        )
        */
        onReset()
      };

      const submitModel = () => {
        const newmodeldata = {
          'model': newmodel.value,
          'brand': newbrand.value,
          'product_number': newnumber.value
        }

        axios.post("http://localhost:8000/api/models", newmodeldata).then(
          response => {
            if (response.status == 201){
              $q.notify({
                color: 'green-4',
                textColor: 'white',
                icon: 'check',
                message: 'Equipo creado con éxito'
              })
              getModels()
              resetModel()
            }
          }, (error) => {
            console.log(error)
          }
        )

      }

      const resetModel = () => {
        newmodel.value = null
        newbrand.value = null
        newnumber.value = null
        newmodelstate.value = false
      }

      return{
        createEquipmentForm,
        name,
        serial,
        inventory,
        model,
        maintenance,
        observation,
        modelOptions,
        newmodelstate,
        newmodel,
        newbrand,
        newnumber,
        newsupplierstate,
        newsuppliername,
        newsupplierrut,
        newsupplieraddress,
        reception_date,
        supplier,
        suppliers,
        suppliersOptions,
        getModels,
        getSuppliers,
        onReset,
        onSubmit,
        submitModel,
        resetModel
      }
    },

    mounted(){
      this.getModels();
      this.getSuppliers();
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
