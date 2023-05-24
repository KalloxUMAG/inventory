<template>
  <q-page padding>
    <div class="row justify-center">
      <q-card class="my-card" flat bordered>
        <q-item class="row justify-center">
          <div class="text-h5">
            {{ supply.name }}
          </div>
        </q-item>
        <q-separator />
        <q-card-section horizontal>
          <q-separator vertical />
          <!--Datos producto-->
          <div class="col">
            <div class="row">Nombre: {{ supply.name }}</div>
            <div class="row">Codigo: {{ supply.code }}</div>
            <div class="row">Costo: {{ supply.cost }}</div>
            <div class="row">Marca: {{ supply.supplies_brand_name }}</div>
            <div class="row">Tipo: {{ supply.supplies_types_name }}</div>
            <div class="row">Proveedor: {{ supply.supplier_name }}</div>
          </div>
          <q-card-section class="col"> </q-card-section>
        </q-card-section>
      </q-card>
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

const getSupply = () => {
  axios
    .get("http://localhost:8000/api/supplies/" + id.value)
    .then((response) => (supply.value = response.data));
};

onMounted(() => {
  getSupply();
});
</script>

<style scoped>
.my-card {
  width: 100%;
}
.field-label {
  font-size: 16px;
  font-weight: bold;
}

.field-content {
  font-size: 16px;
  font-weight: 500;
}

.q-page {
  color: #262626;
}
</style>
