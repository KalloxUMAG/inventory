<template>
  <q-layout view="hHh LpR fFf">
    <q-header bordered class="text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title>
          <div class="text-h4 q-ma-md text-uppercase">
            Sistema de gestión de inventario CADI
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" elevated :width="400">
      <q-scroll-area class="fit">
        <q-list>
          <q-item>
            <div class="text-h4 q-my-sm text-center">
              Sesion iniciada como
              <span class="text-bold">{{ fullname }}</span>
            </div>
          </q-item>
          <template v-for="(menuItem, index) in menuItems" :key="index">
            <q-item
              clickable
              :to="menuItem.to"
              v-ripple
              active-class="my-menu-link"
              :exact="menuItem.exact"
              class=""
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section class="text-weight-bold text-h5">
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
        <footer class="absolute-bottom">
          <small>Fecha de actualización: 05-10-2023</small>
        </footer>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import { menuItems } from "../constants/menuItems.js";
import { useQuasar } from "quasar";

const $q = useQuasar();
const fullname = $q.localStorage.getItem("CATGInventoryFullname");
const leftDrawerOpen = ref(true);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

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
