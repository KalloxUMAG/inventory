<template>
  <div class="info-section">
    <div class="info-section__header q-pa-sm">
      <div class="text-subtitle2 text-weight-bold">
        {{ props.title }}
      </div>
    </div>
    <q-separator />
    <div class="info-section__content">
      <q-list>
        <q-item v-for="field in props.fields" :key="field.label">
          <q-item-section class="col-4">
            <div class="text-caption">
              {{ field.label }}
            </div>
          </q-item-section>
          <q-item-section class="col-1">
            <div class="text-caption">
              :
            </div>
          </q-item-section>
          <q-item-section v-if="field?.type == 'list'" class="col-7">
            <div v-for="value in field.value" :key="value" class="text-body2">
              {{ value }}
            </div>
          </q-item-section>
          <q-item-section v-else class="col-7">
            <div class="text-body2">
              {{ field.value }}
            </div>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
    default: () => (''),
  },
  fields: {
    type: Array,
    required: true,
    default: () => ([]),
  },
})
</script>

<style scoped>
</style>
