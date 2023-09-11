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
  background-color: #eef5f9;
}
</style>
