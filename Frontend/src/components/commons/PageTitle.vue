<template>
  <q-card class="my-card row q-pa-md q-mb-lg justify-between" flat bordered>
    <div class="flex item-title">
      <q-icon :name="icon" size="24px" class="q-mr-sm" />
      <div class="text-subtitle1 text-bold text-uppercase">
        {{ title }}
      </div>
    </div>
    <slot></slot>
  </q-card>
</template>

<script setup>
    const props = defineProps({
        title: String,
        icon: String,
    })
    const { title } = props;
</script>

<style scoped>
.item-title {
  align-content: center;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}
</style>
