<template>
  <q-layout view="hHh lpr lfr">
    <q-header bordered class="bg-primary text-white" height-hint="98">
      <q-tabs align="center" inline-label>
        <q-route-tab
          to="/"
          label="Inicio"
          icon="home"
          active-class="my-menu-link"
          exact
        />
        <q-route-tab
          to="/equipment"
          label="Equipamiento"
          icon="biotech"
          active-class="my-menu-link"
        />
        <q-route-tab
          to="/supplies"
          label="Insumos"
          icon="science"
          active-class="my-menu-link"
        />
        <q-route-tab
          to="/suppliers"
          label="Proveedores"
          icon="store"
          active-class="my-menu-link"
        />
        <q-route-tab
          to="/buildings"
          label="Ubicaciones"
          icon="location_on"
          active-class="my-menu-link"
        />
        <q-route-tab
          to="/projects"
          label="Proyectos"
          icon="schema"
          active-class="my-menu-link"
        />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="scss">
.my-menu-link {
  color: #dcd3e7;
  background: #428f7d;
}
</style>
