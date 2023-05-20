<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
body{
  background-image: url(./assets/background.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}
</style>
