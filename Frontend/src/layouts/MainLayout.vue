<template>
  <q-layout view="hHh LpR fFf">
    <q-header bordered class="bg-primary text-grey" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title>
          Sistema de gestion de inventario CADI
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" elevated>
      <q-scroll-area class="fit">
        <q-list>
          <template v-for="(menuItem, index) in menuItems" :key="index">
            <q-item clickable :to="menuItem.to" v-ripple active-class="my-menu-link" :exact="menuItem.exact" class="">
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section class="text-weight-bold">
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import {menuItems} from "../constants/menuItems.js";

const leftDrawerOpen = ref(true);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

<style lang="scss">
.my-menu-link {
  color: #fff;
  background: rgba(61, 61, 65, 0.9);
}
</style>
