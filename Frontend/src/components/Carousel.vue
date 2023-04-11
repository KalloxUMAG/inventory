<template>
  <q-carousel v-model="slide" animated arrows thumbnails infinite :height="windowHeight" control-color="amber" class="rounded-borders">
    <q-carousel-slide v-if="this.images == null" :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
    <q-carousel-slide v-for="image in images" :key="image.id" :name="image.id" :img-src="image.path"/>
  </q-carousel>
</template>

<script>
import {ref} from 'vue'
import axios from 'axios';


export default {
  data(){
    return{
      images: null,
    }
  },
  methods:{
    getContent(){
      axios.get(this.api).then(
        response => {
          this.images = response.data
        }
      )
    }
  },
  mounted(){
    this.getContent()
  },
  props:{
    api: {
      type: String,
      required: true
    }
  },
  setup(props){
    return{
      slide: ref(1),
      fullscreen: ref(false)
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
