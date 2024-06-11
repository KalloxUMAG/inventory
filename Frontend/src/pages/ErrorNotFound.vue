<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorNotFound',
})
</script>

<template>
  <div
    class="fullscreen bg-blue text-white text-center q-pa-md flex flex-center"
  >
    <div>
      <div style="font-size: 30vh">
        Error 404
      </div>

      <div class="text-h2" style="opacity: 0.4">
        Oops. La página no está disponible o no existe...
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        to="/"
        label="Ir a Inicio"
        no-caps
        icon="home"
      />
    </div>
  </div>
</template>
