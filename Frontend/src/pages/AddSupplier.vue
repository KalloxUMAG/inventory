<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="AddSupplierForm">
        <div class="text-bold text-subtitle1 q-my-sm">Datos proveedor</div>
        <!--Fields-->
        <div v-if="!newsupplierstate">
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
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir proveedor"
              icon="add"
              class="add-btn text-caption"
              @click="newsupplierstate = !newsupplierstate"
            />
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input
              outlined
              v-model="newsuppliername"
              label="Nombre proveedor"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div>
            <q-input
              outlined
              v-model="newsupplierrut"
              label="Rut"
              mask="##.###.###-X"
              unmasked-value
              class="row q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              outlined
              v-model="newsupplieraddress"
              label="Dirección"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              outlined
              v-model="workername1"
              label="Nombre trabajador"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <SelectForm
              outlined
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              @updateModel="(value) => (workerrol1 = value)"
              class="col q-my-sm"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              outlined
              type="email"
              v-model="workermail1"
              label="Correo trabajador"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
          <div class="row">
            <q-input
              outlined
              v-model="workerphone1"
              label="Telefono trabajador"
              mask="(+##) #####-####"
              class="col q-my-sm"
              :disable="disableSupplier"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
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
              @click="notEmptyFields() ? (disableSupplier = true) : ''"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (newsupplierstate = !newsupplierstate),
                  (disableSupplier = false)
              "
            />
          </div>
        </div>
        <div class="row">
          <q-input
            outlined
            v-model="cost"
            type="number"
            label="Costo"
            class="col q-my-sm"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <!--Buttons-->
        <div class="q-mt-sm row justify-end">
          <q-btn
            color="primary"
            label="Guardar"
            type="submit"
            class="q-mr-sm"
          />
          <q-btn color="negative" label="Cancelar" @click="onDialogCancel" />
        </div>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup>
import axios from "axios";
import { sendRequest } from "src/axios/instance.js";
import { useDialogPluginComponent, useQuasar } from "quasar";
import { onMounted, ref, toRefs } from "vue";
import SelectForm from "src/components/SelectForm.vue";
import { rolOptions } from "src/constants/columns.js";

const cost = ref(0);

const disableSupplier = ref(false);

const newsuppliername = ref("");
const newsupplierrut = ref("");
const newsupplieraddress = ref("");

const supplier = ref(null);
const suppliersOptions = ref([]);
const newsupplierstate = ref(false);

const workername1 = ref("");
const workerrol1 = ref("");
const workermail1 = ref("");
const workerphone1 = ref("");

const $q = useQuasar();

const props = defineProps({
  supply_id: Number,
});

const { supply_id } = toRefs(props);
const AddSupplierForm = ref(null);
const api_prefix = process.env.API_URL;

const getSuppliers = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_prefix + "/suppliers",
    });
    const suppliers = response.data;
    suppliersOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name };
    });
  } catch (error) {}
};

function notEmptyFields() {
  return (
    newsuppliername.value != "" &&
    newsupplierrut.value != "" &&
    newsupplieraddress.value != "" &&
    workername1.value != "" &&
    workerrol1.value != "" &&
    workermail1.value != "" &&
    workerphone1.value != ""
  );
}

async function createNewSupplier() {
  if (!newsupplierstate.value) {
    return supplier.value;
  }
  const supplierdata = {
    name: newsuppliername.value,
    rut: newsupplierrut.value,
    city_address: newsupplieraddress.value,
  };
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/suppliers",
      data: supplierdata,
    });
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
  if (!newsupplierstate.value) {
    return;
  }
  if (workername1.value != null) {
    const workerdata = {
      name: workername1.value,
      position: workerrol1.value,
      phone: workerphone1.value,
      email: workermail1.value,
      supplier_id: supplier_id,
    };
    try {
      const response = await sendRequest({
        method: "POST",
        url: api_prefix + "/suppliers_contacts",
        data: workerdata,
      });
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el contacto 1: " + error,
      });
    }
  }
}

onMounted(() => {
  getSuppliers();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

async function onOKClick() {
  AddSupplierForm.value.resetValidation();
  const supplier_id = await createNewSupplier();
  await createNewWorker(supplier_id);
  const data = {
    supplier_id: supplier_id,
    supply_id: props.supply_id,
    cost: cost.value,
  };
  try {
    const response = await sendRequest({
      method: "POST",
      url: api_prefix + "/suppliers_supplies",
      data: data,
    });
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo guardar los cambios: " + error,
    });
    return;
  }
  onDialogOK();
}
</script>
