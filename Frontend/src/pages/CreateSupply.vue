<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent="onSubmit"
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
        ref="createSupplyForm"
      >
        <!--Datos Producto-->
        <h5>Agregar insumos</h5>
        <div class="section-title">
          Datos Insumo
          <hr />
        </div>
        <div class="col">
          <div class="row">
            <q-input
              outlined
              v-model="name"
              label="Nombre"
              class="col q-mr-md"
            />
            <q-input
              outlined
              v-model="code"
              label="Codigo"
              class="col q-mr-md"
            />
            <q-input outlined v-model="cost" label="Valor" class="col" />
          </div>
        </div>
        <div v-if="!newBrandState" class="col">
          <SelectForm
            outlined
            class="row"
            :options="brandOptions"
            option_value="id"
            option_label="name"
            label="Marca"
            not_found_label="No hay marcas disponibles"
            @updateModel="
              (value) => {
                brand = value;
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir marca"
              class="add-btn"
              @click="newBrandState = true"
            />
          </div>
        </div>
        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newBrand"
              class="col"
              label="Marca"
              :disable="disableBrand"
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="disableBrand ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="disableBrand = !disableBrand"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="newBrandState = false"
            />
          </div>
        </div>

        <div v-if="!newTypeState" class="col">
          <SelectForm
            outlined
            class="row"
            :options="typeOptions"
            option_value="id"
            option_label="name"
            label="Tipo de insumo"
            not_found_label="No hay tipos de insumos disponibles"
            @updateModel="
              (value) => {
                type = value;
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir tipo de insumo"
              class="add-btn"
              @click="newTypeState = true"
            />
          </div>
        </div>
        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newType"
              class="col"
              label="Tipo de insumo"
              :disable="disableType"
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              :label="disableType ? 'Editar' : 'Guardar'"
              color="amber"
              class="q-mr-sm"
              @click="disableType = !disableType"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="newTypeState = false"
            />
          </div>
        </div>

        <!--Supplier-->
        <div v-if="!newSupplierState">
          <SelectForm
            outlined
            :options="suppliersOptions"
            option_value="id"
            option_label="name"
            label="Proveedor"
            not_found_label="No hay proveedores disponibles"
            @updateModel="
              (value) => {
                supplier = value;
              }
            "
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir proveedor"
              icon="add"
              class="add-btn text-caption"
              @click="newSupplierState = !newSupplierState"
            />
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newSupplierName"
              label="Nombre proveedor"
              class="col"
              :disable="disableSupplier"
            />
            <q-input
              outlined
              v-model="newSupplierRut"
              label="Rut"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
            <q-input
              outlined
              v-model="newSupplierAddress"
              label="Dirección"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row q-mt-sm">
            <q-input
              outlined
              v-model="workerName1"
              label="Nombre trabajador"
              class="col"
              :disable="disableSupplier"
            />
            <SelectForm
              outlined
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              @updateModel="(value) => (workerRol1 = value)"
              class="col q-ml-md"
            />
            <q-input
              outlined
              v-model="workerMail1"
              label="Correo trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
            <q-input
              outlined
              v-model="workerPhone1"
              label="Telefono trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row q-mt-sm">
            <q-input
              outlined
              v-model="workerName2"
              label="Nombre trabajador"
              class="col"
              :disable="disableSupplier"
            />
            <SelectForm
              outlined
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              @updateModel="(value) => (workerRol2 = value)"
              class="col q-ml-md"
            />
            <q-input
              outlined
              v-model="workerMail2"
              label="Correo trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
            <q-input
              outlined
              v-model="workerPhone2"
              label="Telefono trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn
              v-if="disableSupplier"
              label="Editar"
              color="amber"
              @click="disableSupplier = false"
              class="q-mr-sm"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              @click="disableSupplier = true"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (newSupplierState = !newSupplierState),
                  (disableSupplier = false)
              "
            />
          </div>
        </div>

        <!--Form button-->
        <div class="row justify-end q-mt-mx">
          <q-btn label="Crear" type="submit" color="positive" />
        </div>
        <q-inner-loading
          :showing="loading"
          label="Creando insumo"
          label-class="text-deep-orange"
          label-style="font-size: 1.6em"
        />
      </q-form>
    </div>
  </q-page>
</template>

<script setup>
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";
import SelectForm from "src/components/SelectForm.vue";

//Options Selects
const brandOptions = ref([]);
const suppliersOptions = ref([])
const typeOptions = ref([])
const rolOptions = [
  {
    value: "Vendedor",
    name: "Vendedor",
  },
  {
    value: "Tecnico",
    name: "Tecnico",
  },
];

//Models
const brand = ref(null);
const type = ref(null);
const name = ref(null);
const code = ref(null);
const cost = ref(null);
const newBrand = ref(null);
const newType = ref(null);
const supplier = ref(null)
const newSupplierName = ref(null)
const newSupplierRut = ref(null)
const newSupplierAddress = ref(null)
const workerName1 = ref(null)
const workerRol1 = ref(null)
const workerMail1 = ref(null)
const workerPhone1 = ref(null)
const workerName2 = ref(null)
const workerRol2 = ref(null)
const workerMail2 = ref(null)
const workerPhone2 = ref(null)

//Flags
const disableBrand = ref(false);
const newBrandState = ref(false);
const disableType = ref(false);
const newTypeState = ref(false);
const newSupplierState = ref(false)
const disableSupplier = ref(false)
const loading = ref(false);

//Form
const createSupplyForm = ref(null);
const $q = useQuasar();

const getSuppliesBrands = () => {
  axios.get("http://localhost:8000/api/supplies_brands").then((response) => {
    const supplies_brands = response.data;
    brandOptions.value = supplies_brands.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSuppliesTypes = () => {
  axios.get("http://localhost:8000/api/supplies_types").then((response) => {
    const supplies_types = response.data;
    typeOptions.value = supplies_types.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSuppliers = () => {
  axios.get("http://localhost:8000/api/suppliers").then((response) => {
    const suppliers = response.data;
    suppliersOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

//Create functions

async function createNewBrand(){
  if(!newBrandState.value){
    return brand.value;
  }
  const brandData = {
    name: newBrand.value
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/api/supplies_brands",
      brandData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la marca: " + error,
    });
  }
}

async function createNewType(){
  if(!newTypeState.value){
    return type.value;
  }
  const typeData = {
    name: newType.value
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/api/supplies_types",
      typeData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el tipo de insumo: " + error,
    });
  }
}

async function createNewSupplier() {
  if (!newSupplierState.value) {
    return supplier.value;
  }
  const supplierData = {
    name: newSupplierName.value,
    rut: newSupplierRut.value,
    city_address: newSupplierAddress.value,
  };
  try {
    const response = await axios.post(
      "http://localhost:8000/api/suppliers",
      supplierData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el proveedor: " + error,
    });
  }
}

async function createNewWorker(supplier_id) {
  if (!newSupplierState.value) {
    return;
  }
  if (workerName1.value != null) {
    const workerData1 = {
      name: workerName1.value,
      position: workerRol1.value,
      phone: workerPhone1.value,
      email: workerMail1.value,
      supplier_id: supplier_id,
    };
    try {
      const response = await axios.post(
        "http://localhost:8000/api/suppliers_contacts",
        workerData1
      );
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el contacto 1: " + error,
      });
    }
  }
  if (workerName2.value != null) {
    const workerData2 = {
      name: workerName2.value,
      position: workerRol2.value,
      phone: workerPhone2.value,
      email: workerMail2.value,
      supplier_id: supplier_id,
    };
    try {
      const response = await axios.post(
        "http://localhost:8000/api/suppliers_contacts",
        workerData2
      );
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el contacto 2: " + error,
      });
    }
  }
}


async function createNewSupply(supplyData){
  try {
    const response = await axios.post(
      "http://localhost:8000/api/supplies",
      supplyData
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el insumo: " + error,
    });
  }
}

async function onSubmit() {
  createSupplyForm.value.resetValidation();
  let supplyData = {
    name: name.value,
    code: code.value,
    cost: cost.value,
    supplies_brand_id: brand.value,
    supplier_id: supplier.value,
    supplies_type_id: type.value
  }

  loading.value = true;

  const supplies_brand_id = await createNewBrand();
  if (supplies_brand_id == -1) {
    loading.value = false;
    return;
  }
  supplyData['supplies_brand_id'] = supplies_brand_id;

  const supplies_type_id = await createNewType();
  if (supplies_type_id == -1) {
    loading.value = false;
    return;
  }
  supplyData['supplies_type_id'] = supplies_type_id;

  const supplier_id = await createNewSupplier();
  if (supplier_id == -1) {
    loading.value = false;
    return;
  }
  supplyData["supplier_id"] = supplier_id;
  await createNewWorker(supplier_id);

  const supply_id = await createNewSupply(supplyData)
  if (supply_id == -1) {
    loading.value = false;
    return;
  }

  loading.value = false;
  //Redirect to table
}

onMounted(() => {
  getSuppliesBrands();
  getSuppliesTypes();
  getSuppliers();
});
</script>

<style scoped>
body {
  background-image: url(./../assets/background.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

hr {
  width: 20%;
  height: 2px;
  background-color: black;
}

.q-form {
  margin-top: 10px;
  background-color: #fffffe;
  border-radius: 1%;
  border-width: 1px;
  border-style: solid;
}

.section-title {
  text-align: center;
  font-weight: bold;
  font-size: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

.add-btn {
  background-color: #7b7bd2 !important;
  color: #fff;
  border: 2px solid #7777cf;
}
</style>
