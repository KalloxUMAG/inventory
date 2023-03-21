<template>
  <q-select filled v-model="model" :options="options" :option-value="option_value" :option-label="option_label" emit-value map-options :label="label" @update:model-value="updateModel(model)">
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">
          {{not_found_label}}
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
  import {ref} from 'vue';

  export default {
    emits: ['updateModel'],
    methods: {
      updateModel: function(model) {
        this.$emit('updateModel', model)
      },

    },

    props:{
      options: {
        type: Array,
        required: true
      },
      option_value: {
        type: String,
        required: true
      },
      option_label: {
        type: String,
        required: true
      },
      label: {
        type: String,
        required: true
      },
      not_found_label: {
        type: String,
        required: true
      },
    },

    setup(){
      const model = ref(null)

      return {
        model
      }
    },

    watch: {
      options: function(){
        this.model = null
      }
    }
  }
</script>
