<template>
  <q-carousel
    v-model="slide"
    animated
    arrows
    thumbnails
    infinite
    control-color="amber"
    class="rounded-borders"
  >
    <q-carousel-slide
      v-if="images.length == 0"
      :name="1"
      img-src="https://cdn.quasar.dev/img/mountains.jpg"
    />
    <q-carousel-slide
      v-for="image in images"
      :key="image.id"
      :name="image.id"
      :img-src="api_prefix + image.path"
    />
  </q-carousel>
</template>

<script setup>
import { onMounted, ref, toRefs } from "vue";
import { sendRequest } from "src/axios/instance";

const props = defineProps({
  api_endpoint: String,
});

const api_prefix = process.env.API_URL.slice(0, -4);
const { api_endpoint } = toRefs(props);

const slide = ref(1);
const images = ref([]);

const getContent = async () => {
  try {
    const response = await sendRequest({
      method: "GET",
      url: api_endpoint.value,
    });
    images.value = response.data;
  } catch (error) {}
};

onMounted(() => {
  getContent();
});
</script>

<style lang="scss" scoped>
.q-carousel__slide {
  max-width: 100%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
