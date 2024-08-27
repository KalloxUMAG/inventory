<template>
  <q-item class="q-pa-none" :style="style">
    <q-item-section class="justify-center q-pa-md q-ml-none text-white">
      <q-item-label class="text-white text-h6 text-weight-bolder">{{ value }}</q-item-label>
      <q-item-label>{{ title }}</q-item-label>
    </q-item-section>
    <q-item-section class="justify-center q-mr-md text-white" side>
      <q-icon :name="icon" size="50px" color="white" />
    </q-item-section>
  </q-item>
</template>

<script setup>
import { computed, toRefs } from 'vue'

const props = defineProps({
  color: {
    type: String,
    default: '#e54d21',
  },
  icon: {
    type: String,
    default: 'package_2',
  },
  title: {
    type: String,
    default: 'Título',
  },
  value: {
    type: Number,
    default: 0,
  },
})

const { color, icon, title, value } = toRefs(props)

const style = computed(() => {
  return `background-color: ${color.value}`
})
</script>

<style scoped>
.q-item {
  height: 100%;
}
</style>
