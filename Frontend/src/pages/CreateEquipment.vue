<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form @submit.prevent="onSubmit" @reset="onReset" class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pt-xl" ref="createEquipmentForm">
        <q-input filled v-model="name" maxlength="49" label="Nombre del equipo" lazy-rules
        :rules="[
          val => val && val.length > 0 || 'Este campo es obligatorio',
          val => val && val.length < 50 || 'El nombre debe contener menos de 50 caracteres'
        ]"/>
        <q-input filled v-model="reception_date" type="date" label="Fecha de recepción" stack-label lazy-rules :rules="[val => val && val != null || 'Este campo es obligatorio']"/>
        <q-input filled v-model="serial" maxlength="30" label="Código serial" lazy-rules
          :rules="[
            val => val && val.length > 0 || 'Este campo es obligatorio',
            val => val && val.length < 31 || 'Máximo 30 caracteres'
          ]"/>
        <q-input filled v-model="inventory" maxlength="9" type="number" label="Inventario UMAG" lazy-rules :rules="[val => val < 999999999 || 'El número máximo es 999999999']"/>
        <q-select filled v-model="model" :options="modelOptions" option-value="id" option-label="name" emit-value map-options label="Modelo">
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
              <q-input class="col" label="Número de Producto" v-model="newnumber" lazy-rules/>
            </div>
            <div class="row justify-end q-pt-sm q-pb-md">
              <q-btn label="Crear" type="submit" color="primary"/>
              <q-btn label="Cancelar" type="reset" color="negative" class="q-ml-sm" @click="this.newmodelstate = !this.newmodelstate"/>
            </div>
          </q-form>
        </div>

        <q-input filled v-model="maintenance" type="number" label="Periodo de mantención (días)" lazy-rules/>
        <q-input filled v-model="observation" type="textarea" label="Observación" lazy-rules/>
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
    data(){
      return{
        models: []
      }
    },
    methods: {
      getModels(){
        axios.get("http://localhost:8000/api/models").then(
          response => {
            this.models = response.data
            this.modelOptions = this.models.map(x => {
              return {id: x.id, name: x.brand+" "+x.model+" "+x.product_number}
            })
            console.log(this.modelOptions)
          }
        )
      }
    },
    setup(){
      const createEquipmentForm = ref(null)
      const name = ref(null)
      const serial = ref(null)
      const inventory = ref(null)
      const model = ref(null)
      const maintenance = ref(null)
      const observation = ref(null)
      const modelOptions = ref([])
      const newmodelstate = ref(false)
      const newmodel = ref(null)
      const newbrand = ref(null)
      const newnumber = ref(null)
      const reception_date = ref(null)
      const $q = useQuasar()

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
        console.log(reception_date.value)
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
            }
          }, (error) => {
            console.log(error)
          }
        )
        resetModel()
        this.getModels().then();
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
        reception_date,
        onReset,
        onSubmit,
        submitModel,
        resetModel
      }
    },

  mounted(){
  this.getModels();
},

  }


</script>
