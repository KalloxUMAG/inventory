<template>
  <q-carousel v-model="slide" transition-prev="slide-right" transition-next="slide-left" swipeable animated control-color="amber" navigation padding arrows height="300px">
    <q-carousel-slide :name="1" class="column no-wrap">
      <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
        <q-img class="rounded-borders col-6 full-height" src="http://localhost:8000/images/equipments/2/belfast.png" />
        <q-img class="rounded-borders col-6 full-height" src="https://cdn.quasar.dev/img/parallax1.jpg" />
      </div>
    </q-carousel-slide>
    <q-carousel-slide v-for="image in images" :key="image.name" :name="2" :img-src="image.path"/>

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
        response => (
          this.images = response.data
        )
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
      slide: ref(1)
    }
  }
}
</script>
