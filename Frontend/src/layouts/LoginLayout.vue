<template>
  <q-layout view="hHh LpR fFf">
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.bg-image {
  background-image: url('/images/cadi_building.jpg');
  background-size: cover;
  background-position: center;
}
</style>
