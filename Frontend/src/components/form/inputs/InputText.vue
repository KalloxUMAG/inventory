<template>
    <q-input
      :model-value="modelValue"
      @update:model-value="updateModelValue"
      :outlined="outlined"
      :type="type"
      :label="label"
      :class="inputClass"
      :rules="rules"
      lazy-rules
      :bg-color="bgColor"
    />
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    modelValue: {
      type: [String, Number],
      required: true,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    type: {
      type: String,
      default: 'text',
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
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  function updateModelValue(value) {
    emit('update:modelValue', value)
  }
  </script>