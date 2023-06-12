<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form @submit="onOKClick" ref="AddSupplierForm">
        <div class="text-bold text-subtitle1 q-my-sm">Datos lote</div>
        <!--Fields-->
        <div class="col">
          <div class="row q-my-sm">
            <SelectForm
              outlined
              class="col"
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
          </div>
          <div class="row q-my-sm">
            <q-input
              outlined
              v-model="number"
              label="Número"
              class="col q-mr-sm"
            />
            <q-input
              outlined
              v-model="stock"
              label="Stock"
              class="col q-ml-sm"
            />
          </div>
          <div class="row q-my-sm">
            <q-input
              outlined
              class="col"
              v-model="reception_date"
              type="date"
              label="Fecha de recepción*"
              stack-label
              lazy-rules
              :rules="[
                (val) => (val && val != null) || 'Este campo es obligatorio',
              ]"
            />
          </div>
          <div class="row">
            <q-input
              outlined=""
              class="col"
              type="text"
              stack-label
              label="Observacion"
              v-model="observation"
            />
          </div>
          <div class="row">
            <div v-if="!newLocationState" class="col q-mr-md">
              <SelectForm
                outlined
                class="row q-mr-md"
                :disable="disableLocation"
                :options="locationOptions"
                option_value="id"
                option_label="name"
                label="Localizacion"
                not_found_label="No hay localizaciones disponibles"
                @updateModel="
                  (value) => {
                    location = value;
                  }
                "
              />
              <div class="row justify-end q-pt-md">
                <q-btn
                  label="Añadir localizacion"
                  icon="add"
                  class="add-btn text-caption q-mr-md"
                  @click="newLocationState = !newLocationState"
                />
              </div>
            </div>
            <div v-else class="col">
              <div class="row">
                <q-input
                  outlined
                  v-model="newLocation"
                  label="Nombre localizacion"
                  class="col"
                  :disable="disableLocation"
                />
              </div>
            </div>
            <div
              v-if="!newLocationState && !newSublocationState"
              class="col q-mr-md"
            >
              <SelectForm
                outlined
                class="row q-mr-md"
                :disable="disableSublocation"
                :options="sublocationOptions"
                option_value="id"
                option_label="name"
                label="Sub-localizacion"
                not_found_label="No hay sublocalizaciones disponibles"
                @updateModel="
                  (value) => {
                    sublocation = value;
                  }
                "
              />
              <div class="row justify-end q-pt-md">
                <q-btn
                  outlined
                  label="Añadir sub-localizacion"
                  icon="add"
                  class="add-btn text-caption q-mr-md"
                  @click="newSublocationState = !newSublocationState"
                />
              </div>
            </div>
            <div v-else class="col q-pl-md">
              <div class="row">
                <q-input
                  outlined
                  v-model="newSublocation"
                  label="Nombre sub-localizacion"
                  class="col"
                  :disable="disableLocation"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div v-if="newLocationState || newSublocationState" class="row justify-end">
            <q-btn
              v-if="disableLocation"
              label="Editar"
              color="amber"
              @click="disableLocation = false"
              class="q-mr-sm"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              @click="disableLocation = true"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (newLocationState = false),
                  (newSublocationState = false),
                  (disableLocation = false)
              "
            />
          </div>
        </div>
        <!--Buttons-->
        <div class="q-mt-md row justify-end">
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
const api_prefix = process.env.API;

const number = ref(null);
const stock = ref(null);
const supplier = ref(null);
const observation = ref(null);
const reception_date = ref(null);
const location = ref(null);
const sublocation = ref(null);

const newLocationState = ref(false);
const disableLocation = ref(false);
const newSublocationState = ref(false);
const disableSublocation = ref(false);
const newLocation = ref(null);
const newSublocation = ref(null);

const suppliersOptions = ref([]);
const locationOptions = ref([]);
const sublocationOptions = ref([]);

const $q = useQuasar();

const props = defineProps({
  supply_id: Number,
});

const getSuppliers = () => {
  axios
    .get(api_prefix + "/suppliers_supplies/" + props.supply_id)
    .then((response) => (suppliersOptions.value = response.data));
};

onMounted(() => {
  getSuppliers();
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

async function onOKClick() {
  AddSupplierForm.value.resetValidation();

  const data = {
    supplier_id: supplier.value,
    number: number.value,
    due_date: due_date.value,
    stock: stock.value,
    observation: observation.value,
    sub_location_id: sub_location.value,
    project_id: project.value,
    supply_id: props.supply_id,
  };
  onDialogOK();
}
</script>
