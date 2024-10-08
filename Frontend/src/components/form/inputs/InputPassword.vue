<template>
    <q-input
      :autocomplete="autocomplete"
      :model-value="modelValue"
      @update:model-value="updateModelValue"
      :outlined="outlined"
      :type="showPassword ? 'text' : 'password'"
      :label="label"
      :class="inputClass"
      :rules="rules"
      lazy-rules
      :bg-color="bgColor"
    >
        <template #prepend  v-if="icon">
          <q-icon name="key" />
        </template>   
        <template v-slot:append>
          <q-icon
            :name="showPassword ? 'visibility' : 'visibility_off'"
            class="cursor-pointer"
            @click="showPassword = !showPassword"
          />
        </template>
    </q-input>
  </template>
  
  <script setup>
  import { ref, defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    modelValue: {
      type: [String, Number],
      required: true,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      required: true,
    },
    inputClass: {
      type: String,
      default: '',
    },
    rules: {
      type: Array,
      default: () => [],
    },
    bgColor: {
      type: String,
      default: '',
    },
    icon: {
        type: Boolean,
        default: true,
    },
    autocomplete: {
        type: String,
        default: '',
    },
  })
  
  const showPassword = ref(false)

  const emit = defineEmits(['update:modelValue'])
  
  function updateModelValue(value) {
    emit('update:modelValue', value)
  }
  </script>