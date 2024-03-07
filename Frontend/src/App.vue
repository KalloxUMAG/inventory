<template>
  <router-view />
</template>

<script>
import { createApp, defineComponent } from "vue";

const app = defineComponent({
  name: "App",
});

export default app;
</script>

<style lang="scss">
@import "./css/quasar.variables.scss";
body {
  background-color: #e7eae7da;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}
</style>
