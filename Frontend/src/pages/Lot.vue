<template>
  <div class="row justify-center">
    <q-card class="my-card" flat bordered>
      <q-item class="row justify-center">
        <div class="text-h5">
          {{ lot.number }}
        </div>
      </q-item>
      <q-separator />
      <q-card-section horizontal>
        <q-separator vertical />
        <!-- Datos producto -->
        <div class="col">
          <div class="row">
            Insumo: {{ lot.supply_name }}
          </div>
          <div class="row">
            Codigo: {{ lot.supply_code }}
          </div>
          <div class="row">
            Lote: {{ lot.number }}
          </div>
          <div class="row">
            Fecha vencimiento: {{ lot.due_date }}
          </div>
          <div class="row">
            Localizacion: {{ lot.location }}
          </div>
          <div class="row">
            Sub-localizacion: {{ lot.sub_location }}
          </div>
          <div class="row">
            Stock: {{ lot.stock }}
          </div>
          <div class="row">
            Proveedor: {{ lot.supplier_name }}
          </div>
          <div class="row">
            Observacion: {{ lot.observations }}
          </div>
        </div>
        <q-card-section class="col" />
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import { sendRequest } from 'src/axios/instance'

const route = useRoute()
const id = computed(() => route.params.id)
const lot = ref({})

const api_prefix = process.env.API_URL

async function getLot() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/lots/${id.value}`,
    })
    lot.value = response.data
  }
  catch (error) {}
}

onMounted(() => {
  getLot()
})
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
</style>
