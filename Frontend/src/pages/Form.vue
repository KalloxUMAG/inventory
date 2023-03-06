<template>
    <q-page>
        <h4>Agregar Productos</h4>
        <pre>{{ producto }} - {{ seleccion }}</pre>
        <q-form class="row q-col-gutter-md" @submit.prevent="procesarFormulario" @reset="reset" ref="myForm">
            <div class="col-12 col-sm-6">
                <q-input label="Producto" v-model="producto" :rules="[ val => val && val.length > 0 || 'Please type something']" lazy-rules/> 
            </div>
            <div class="col-12 col-sm-6">
                <q-select label="Prioridad" v-model="seleccion" :options="opciones" :rules="[ val => val && val.length > 0 || 'Please select something']" lazy-rules/> 
            </div>
            <div class="col-12">
                <q-toggle label="Aceptar los terminos" v-model="terminos"/>
            </div>
            <div class="col-12">
                <q-btn color="primary" label="Submit" type="submit"/>
                <q-btn color="primary" label="Reset" outline class="q-ml-sm" :ripple="false" type="reset"/>
            </div>
        </q-form>
        <PintarDatos :productos="productos"/>
    </q-page>
</template>

<script>
import { ref } from 'vue';
import {useQuasar} from 'quasar'
import PintarDatos from "src/components/PintarDatos.vue"

export default{
    components: {PintarDatos},
    setup(){
        const $q = useQuasar()
        const producto = ref(null)
        const seleccion = ref(null)
        const terminos = ref(false)
        const myForm = ref(null)
        const opciones = ['maxima', 'moderada', 'minima']

        const productos = ref([])

        const procesarFormulario = () => {
            if(terminos.value === false){
                $q.notify({
                    color: 'red-5',
                    textColor: 'white',
                    icon: 'warning',
                    message: "No se han aceptado los terminos"
                })
            }else{
                $q.notify({
                    color: 'green-5',
                    textColor: 'white',
                    icon: 'check',
                    message: "Exito"
                })

                //Procesar el formulario
                productos.value = [...productos.value, {producto: producto.value, prioridad: seleccion.value}]

                //Reset del formulario
                myForm.value.resetValidation()
                
                reset()

                
            }
        }

        const reset = () => {
            console.log("Hello world")
            producto.value = null
            seleccion.value = null
            terminos.value = false
        }

        return {
            producto,
            seleccion,
            opciones,
            procesarFormulario,
            terminos,
            reset,
            myForm,
            productos
        }
    }
}
</script>