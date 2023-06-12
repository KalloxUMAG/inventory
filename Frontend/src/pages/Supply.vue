<template>
  <q-page padding>
    <div class="row q-col-gutter-md">
      <div class="flex col">
        <q-card class="my-card fit" flat bordered>
          <q-item class="row justify-center">
            <div class="text-h5 text-weight-bold">Datos insumo</div>
          </q-item>
          <q-separator />
          <!--Datos producto-->
          <q-card-section>
            <div class="col q-pa-sm">
              <div class="row q-mb-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Nombre</div>
                <div class="col text-h6 text-grey-8">{{ supply.name }}</div>
              </div>
              <q-separator/>
              <div class="row q-my-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Código</div>
                <div class="col text-h6 text-grey-8">{{ supply.code }}</div>
              </div>
              <q-separator/>
              <div class="row q-my-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Marca</div>
                <div class="col text-h6 text-grey-8">{{ supply.supplies_brand_name }}</div>
              </div>
              <q-separator/>
              <div class="row q-my-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Tipo</div>
                <div class="col text-h6 text-grey-8">{{ supply.supplies_type_name }}</div>
              </div>
              <q-separator/>
              <div class="row q-my-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Stock actual</div>
                <div class="col text-h6 text-grey-8">{{ supply.stock }} unidades</div>
              </div>
              <q-separator/>
              <div class="row q-mt-sm">
                <div class="col-3 text-h6 text-weight-bold q-pl-md">Stock crítico</div>
                <div class="col text-h6 text-grey-8">{{ supply.critical_stock }}</div>
              </div>

            </div>
          </q-card-section>
        </q-card>
      </div>
      <div class="flex col">
        <q-card class="my-card fit" flat bordered>
          <q-card-section horizontal>
            <q-separator vertical />
            <!--Datos producto-->
            <div class="col">
              <NoRedirectTable
                title="Proveedores"
                :columns="suppliersSupplyColumns"
                :rows="suppliers"
                :addFunction="addSupplier"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
    <div class="row q-mt-md">
      <div class="col">
        <NoRedirectTable title="Lotes" :columns="lotsColumns" :rows="[]" :addFunction="addLot"/>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed, onMounted, ref } from "vue";
import axios from "axios";
import NoRedirectTable from "src/components/NoRedirectTable.vue";
import AddSupplier from "./AddSupplier.vue"; 
import AddLot from "./AddLot.vue";
import { suppliersSupplyColumns, lotsColumns } from "../constants/columns.js";
import { useQuasar } from "quasar";

const route = useRoute();
const id = computed(() => route.params.id);
const supply = ref({});
const suppliers = ref([])

const $q = useQuasar();

const api_prefix = process.env.API;

const getSupply = () => {
  axios
    .get(api_prefix + "/supplies/" + id.value)
    .then((response) => (supply.value = response.data));
};

const getSuppliers = () => {
  axios.get(api_prefix+"/suppliers_supplies/"+id.value).then((response) => (suppliers.value = response.data));
}

function addSupplier() {
  $q.dialog({
    component: AddSupplier,
    componentProps: {
      supply_id: supply.value.id,
    },
  }).onOk((data) => {});
}

function addLot() {
  $q.dialog({
    component: AddLot,
    componentProps: {
      supply_id: supply.value.id,
    },
  }).onOk((data) => {});
}

onMounted(() => {
  getSupply();
  getSuppliers();
});
</script>

<style scoped>
.field-label {
  font-size: 16px;
  font-weight: bold;
}

.field-content {
  font-size: 16px;
  font-weight: 500;
}

.col {
  height: 100%;
}

.q-page {
  color: #262626;
}
</style>
