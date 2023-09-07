<template>
  <router-view />
</template>

<script>
import { createApp ,defineComponent } from 'vue'
import { createStore} from 'vuex'


const store = createStore({
  state(){
    return {
      count: 0
    }
  },
  mutations: {
    increment(state){
      state.count++
    }
  }
})

const app = defineComponent({
  name: 'App', 
})

export default app
</script>

<style lang="scss">
@import './css/quasar.variables.scss';
body{
  background-color: #eef5f9;
}
</style>
