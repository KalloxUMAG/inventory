<template>
  <q-layout view="Lhh lpR lFf">
    <q-header bordered class="text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" color="secondary" @click="toggleLeftDrawer" />
        <BreadCrumb />
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
          <q-item class="drawer-message-container">
            <div class="image-container">
              <img src="/images/cadi_inv.webp">
            </div>
          </q-item>
          <template v-for="(menuItem, index) in menuItems" :key="index">
            <q-item v-if="menuItem.type === 'label'" class="menu-label">
              {{ menuItem.label }}
            </q-item>
            <q-item
              v-if="menuItem.type === 'nav'"
              v-ripple
              clickable
              :to="menuItem.to"
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
            <q-separator v-if="menuItem.separator" :key="`sep${index}`" />
          </template>
        </q-list>

        <footer class="fixed-bottom text-white">
          <small>Fecha de actualización: 11-06-2024</small>
        </footer>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-lg">
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { menuItems } from '../constants/menuItems.js'
import BreadCrumb from '../components/commons/BreadCrumb.vue'

const $q = useQuasar()
const fullname = $q.localStorage.getItem('CATGInventoryFullname')
const leftDrawerOpen = ref(true)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
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

.drawer-message-container {
  background-color: var(--drawer-menu-label-bg-color);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item-icon {
  font-size: 1.5rem;
}

.item-text {
  font-size: 1rem;
}

.image-container {
  width: 100%;
  padding: 10px;
  img {
    width: 100%;
  }
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
