<template>
  <q-layout view="hHh LpR fFf">
    <q-header bordered class="text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <div class="text-h4 q-ma-md text-uppercase">Sistema de gestión de inventario CADI</div>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>

</script>

<style lang="scss">
.q-header{
  background-color: #2196f3;
}

.q-drawer{
  background-color: #ffffff;
}

.my-menu-link {
  color: #fff;
  background: rgba(0, 0, 0, 0.9);
}
</style>
