<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin q-pa-md">
      <q-form @submit="onOKClick" ref="EditEquipmentPurchaseForm">
        <div class="text-bold text-subtitle1">Datos compra</div>
        <!--Fields-->
        <SelectForm
          :options="supplierOptions"
          option_value="id"
          option_label="name"
          label="Proveedor"
          not_found_label="No hay proveedores disponibles"
          :default_value="supplier_value"
          @updateModel="
            (value) => {
              supplier = value;
              getInvoices();
            }
          "
        />
        <q-input
          v-model="reception_date"
          type="date"
          label="Fecha de recepción*"
          stack-label
          lazy-rules
          :rules="[
            (val) => (val && val != null) || 'Este campo es obligatorio',
          ]"
        />
        <SelectForm
          :options="invoiceOptions"
          option_value="id"
          option_label="name"
          label="Número de factura"
          not_found_label="No hay facturas disponibles"
          :default_value="invoice_value"
          @updateModel="
            (value) => {
              invoice = value;
            }
          "
        />
        <SelectForm
          :options="projectOptions"
          option_value="id"
          option_label="name"
          label="Proyecto"
          not_found_label="No hay proyectos disponibles"
          :default_value="project_value"
          @updateModel="
            (value) => {
              project = value;
              getStages();
            }
          "
        />
        <SelectForm
          :options="stageOptions"
          option_value="id"
          option_label="name"
          label="Etapa"
          not_found_label="No hay etapas disponibles"
          :default_value="stage_value"
          @updateModel="
            (value) => {
              stage = value;
            }
          "
        />
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
import { useDialogPluginComponent, useQuasar } from "quasar";
import { onMounted, ref, toRefs } from "vue";
import SelectForm from "src/components/SelectForm.vue";

const $q = useQuasar();

const props = defineProps({
  id: Number,
  supplier_value: Object,
  reception_date_value: String,
  invoice_value: Object,
  project_value: Object,
  stage_value: Object,
});

const {
  id,
  supplier_value,
  reception_date_value,
  invoice_value,
  project_value,
  stage_value,
} = toRefs(props);

const supplier = ref(supplier_value.value.id);
const reception_date = ref(reception_date_value.value);
const invoice = ref(invoice_value.value.id);
const project = ref(project_value.value.id);
const stage = ref(stage_value.value.id);

const supplierOptions = ref([]);
const invoiceOptions = ref([]);
const projectOptions = ref([]);
const stageOptions = ref([]);

const EditEquipmentPurchaseForm = ref(null);

const api_prefix = process.env.API;

const getSuppliers = () => {
  axios.get(api_prefix + "/suppliers").then((response) => {
    const suppliers = response.data;
    supplierOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getInvoices = () => {
  if (supplier.value === null) {
    invoiceOptions.value = [];
    invoice.value = null;
  } else {
    axios
      .get(api_prefix + "/invoices/supplier/" + supplier.value)
      .then((response) => {
        const invoices = response.data;
        invoiceOptions.value = invoices.map((x) => {
          return { id: x.id, name: x.number };
        });
      });
  }
};

const getProjects = () => {
  axios.get(api_prefix + "/projects").then((response) => {
    const projects = response.data;
    projectOptions.value = projects.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getStages = () => {
  if (project.value === null) {
    stageOptions.value = [];
    stage.value = null;
  } else {
    axios.get(api_prefix + "/stages/" + project.value).then((response) => {
      const stages = response.data;
      stageOptions.value = stages.map((x) => {
        return { id: x.id, name: x.name };
      });
    });
  }
};

onMounted(() => {
  getSuppliers();
  getInvoices();
  getProjects();
  getStages();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
// dialogRef      - Vue ref to be applied to QDialog
// onDialogHide   - Function to be used as handler for @hide on QDialog
// onDialogOK     - Function to call to settle dialog with "ok" outcome
//                    example: onDialogOK() - no payload
//                    example: onDialogOK({ /*...*/ }) - with payload
// onDialogCancel - Function to call to settle dialog with "cancel" outcome

// this is part of our example (so not required)
async function onOKClick() {
  // on OK, it is REQUIRED to
  // call onDialogOK (with optional payload)
  EditEquipmentPurchaseForm.value.resetValidation();
  const data = {
    id: props.id,
    supplier_id: supplier.value,
    reception_date: reception_date.value,
    invoice_id: invoice.value,
  };
  try {
    const response = await axios.put(
      api_prefix + "/equipments/" + data.id,
      data
    );
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
  // or with payload: onDialogOK({ ... })
  // ...and it will also hide the dialog automatically
}
</script>
