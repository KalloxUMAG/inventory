<template>
  <q-layout view="hHh LpR fFf">
    <q-page-container>
      <q-page class="q-pa-lg bg-grey-2">
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup></script>

<style lang="scss">
.q-header {
  background-color: #2196f3;
}

.q-drawer {
  background-color: #ffffff;
}

.my-menu-link {
  color: #fff;
  background: rgba(0, 0, 0, 0.9);
}
</style>
