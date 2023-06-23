<template>
  <q-carousel v-model="slide" animated arrows thumbnails infinite control-color="amber" class="rounded-borders">

      <q-carousel-slide v-if="images.length == 0" :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
      <q-carousel-slide v-for="image in images" :key="image.id" :name="image.id" :img-src="image.path"/>


  </q-carousel>
</template>

<script setup>
import {onMounted, ref, toRefs} from 'vue'
import axios from 'axios';

const props = defineProps({
  api_endpoint: String,
});

const { api_endpoint } = toRefs(props);

const slide = ref(1)
const images = ref([]);

const getContent = () => {
  axios.get(api_endpoint.value).then(
        (response) => (
          images.value = response.data
        )
      )
}

onMounted(() => {
  getContent();
})

</script>

<style lang="scss" scoped>
  .q-carousel__slide{
    background-size: 100% 100%;
    background-repeat: no-repeat;
  }
</style>
