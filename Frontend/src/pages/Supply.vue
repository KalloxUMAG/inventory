<template>
  <q-page padding>
    <div class="row q-col-gutter-md">
      <div class="flex col-7">
        <q-card class="my-card fit" flat bordered>
          <q-item class="row justify-center">
            <div class="text-h5">Insumo</div>
          </q-item>
          <q-separator />
          <q-card-section horizontal>
            <q-separator vertical />
            <!--Datos producto-->
            <div class="col">
            <div class="row">
              <div class="col">
                <div class="row">Nombre:</div>
                <div class="row">{{ supply.name }}</div>
              </div>
              <div class="col">
                <div class="row">Codigo:</div>
                <div class="row">{{ supply.code }}</div>
              </div>
              <div class="col">
                <div class="row">Costo:</div>
                <div class="row">{{ supply.cost }}</div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <div class="row">Marca:</div>
                <div class="row">{{ supply.supplies_brand_name }}</div>
              </div>
              <div class="col">
                <div class="row">Tipo:</div>
                <div class="row">{{ supply.supplies_type_name }}</div>
              </div>
              <div class="col">
                <div class="row">Cantidad actual:</div>
                <div class="row">{{ supply.stock }}</div>
              </div>
            </div>
          </div>
          </q-card-section>
        </q-card>
      </div>
      <div class="flex col-5">
        <q-card class="my-card fit" flat bordered>
          <q-item class="row justify-center">
            <div class="text-h5">Proveedores</div>
          </q-item>
          <q-separator />
          <q-card-section horizontal>
            <q-separator vertical />
            <!--Datos producto-->
            <div class="col">Tabla proveedores</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed, onMounted, ref } from "vue";
import axios from "axios";
import NoRedirectTable from "src/components/NoRedirectTable.vue";

const route = useRoute();
const id = computed(() => route.params.id);
const supply = ref({});

const api_prefix = process.env.API;

const getSupply = () => {
  axios
    .get(api_prefix + "/supplies/" + id.value)
    .then((response) => (supply.value = response.data));
};

onMounted(() => {
  getSupply();
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
