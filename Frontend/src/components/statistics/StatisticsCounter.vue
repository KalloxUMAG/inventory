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
.statistic-container {
  align-items: center;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12);
  display: flex;
  height: 90px;
  justify-content: center;
  overflow: hidden;
  width: 200px;
  min-width: 200px;
}

.statistic-icon {
  align-items: center;
  background-color: #e54d21;
  display: flex;
  height: 90px;
  justify-content: center;
  width: 90px;
}

.statistic-info {
  align-items: center;
  background-color: white;
  display: flex;
  flex-direction: column;
  height: 90px;
  justify-content: center;
  width: 110px;
  .statistic-value {
    font-size: 20px;
    font-weight: bold;
    margin: 0px;
    text-align: center;
  }
  .statistic-title {
    font-size: 12px;
    margin: 0px;
    text-align: center;
  }
}
</style>
