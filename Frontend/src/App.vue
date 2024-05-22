<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

const app = defineComponent({
  name: 'App',
})

export default app
</script>

<style lang="scss">
@import "./css/quasar.variables.scss";
body {
  background-color: var(--background-color);
  font-family: var(--font-family);
}
</style>
