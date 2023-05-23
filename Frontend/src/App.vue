<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style lang="scss">
@import './css/quasar.variables.scss';
body{
  background-color: $light-page;
}
</style>
