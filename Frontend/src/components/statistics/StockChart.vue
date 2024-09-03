<template>
  <div>
    <div class="row q-col-gutter-md">
      <div v-for="group in data" :key="group.group_id" class="col-6 col-md-3">
        <q-card class="no-shadow q-pa-xs card_style full-height" flat bordered>
          <q-card-section class="text-h6 text-weight-bold text-center">
            <div class="text-subtitle2 text-grey-7">
              Grupo
            </div>
            <span>{{ group.group_name }}</span>
            <div v-if="group.quantity <= critical">
              <q-badge label="Bajo stock" color="red" text-color="white" />
            </div>
          </q-card-section>
          <q-card-section class="text-h3 text-bolder text-center">
            <div class="text-subtitle2 text-grey-7">
              Stock
            </div>
            <span>{{ group.quantity }}</span>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  data: Array,
  critical: Number,
})
const data = props.data
</script>

<style scoped>
  .card_style {
    border-radius: 12px;
  }

  .full-height {
    height: 100%;
  }
</style>
