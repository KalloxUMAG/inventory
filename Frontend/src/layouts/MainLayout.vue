<template>
  <q-layout view="hHh LpR fFf">
    <q-header bordered class="text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title>
          <div class="text-h4 q-ma-md q-ml-md">
            Sistema de gestión de inventario CADI
          </div>
        </q-toolbar-title>
        <q-btn
          to="/login"
          flat
          align="between"
          size="lg"
          class="q-mr-md"
          icon="logout"
          label="Cerrar session"
        />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" elevated :width="275">
      <q-scroll-area class="fit">
        <q-list>
          <q-item>
            <div class="text-h5 text-white q-my-sm text-center">
              Sesion iniciada como
              <span class="text-bold">{{ fullname }}</span>
            </div>
          </q-item>
          <template v-for="(menuItem, index) in menuItems" :key="index">
            <q-item v-if="menuItem.type == 'label'" class="menu-label">
              {{ menuItem.label }}
            </q-item>
            <q-item
              v-if="menuItem.type == 'nav'"
              clickable
              :to="menuItem.to"
              v-ripple
              class="menu-link"
              active-class="active-menu-link"
              :exact="menuItem.exact"
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" size="2.5rem" />
              </q-item-section>
              <q-item-section class="text-subtitle1">
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
        <q-img src="/src/assets/cadi.png" width="90%" class="q-ml-md q-mt-lg" />
        <footer class="fixed-bottom text-white">
          <small>Fecha de actualización: 17-10-2023</small>
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
  background-color: rgb(109, 86, 160);
  background-color: #5e3bbf;
  background-color: #324580;
}

.q-drawer {
  background-color: #022140;
}

.menu-label {
  color: #d5d2d2;
}

.menu-link {
  color: #dfdfdf;
}

.active-menu-link {
  color: #ffffff;
  background: rgba(100, 76, 152, 0.659);
}
</style>
