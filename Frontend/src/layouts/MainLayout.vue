<template>
  <q-layout view="Lhh lpR lFf">
    <q-header bordered class="text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" class="hidden" @click="toggleLeftDrawer" />
        <q-btn
          to="/login"
          flat
          align="between"
          size="lg"
          class="q-mr-md absolute-right text-black"
          icon="logout"
          label="Cerrar session"
        />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" show-if-above :width="300">
      <q-scroll-area class="fit">
        <q-list>
          <q-item>
            <div class="drawer-message q-my-sm">
              Inventario CADI
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
                <q-icon :name="menuItem.icon" class="item-icon" />
              </q-item-section>
              <q-item-section class="item-text">
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
        <div class="image-container">
          <q-img src="/src/assets/cadi.webp" width="100%"/>
        </div>

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
.header-title {
  font-size: 1.5rem;
}

.drawer-message {
  font-size: 1.4rem;
  color: var(--drawer-menu-label-text-color);
  text-align: center;
  width: 100%;
  text-transform: uppercase;
}

.item-icon {
  font-size: 1.5rem;
}

.item-text {
  font-size: 1rem;
}

.image-container {
  padding: 10px;
}

.q-header {
  background-color: var(--header-bg-color);
}

.q-drawer {
  background-color: var(--drawer-bg-color);
}

.q-item__section--avatar{
  min-width: unset;
}

.menu-label {
  color: var(--drawer-menu-label-text-color);
  flex-wrap: wrap;
  align-content: end;
}

.menu-link {
  color: var(--drawer-menu-link-text-color);

}

.active-menu-link {
  color: var(--drawer-active-menu-link-color);
  background: var(--drawer-active-menu-link-bg-color);
}
</style>
