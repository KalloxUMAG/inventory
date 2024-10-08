<template>
  <q-select
    outlined
    bg-color="white"
    v-model="model"
    :options="stringOptions"
    :option-value="option_value"
    :option-label="option_label"
    emit-value
    map-options
    :label="label"
    use-input
    input-debounce="0"
    :clearable="clearable"
    :rules="required ? [val => !!val || 'Campo obligatorio'] : []"
    @update:model-value="updateModel(model)"
  >
    <template #before-options>
      <div class="q-pa-sm">
        <q-input v-model="filter" dense outlined placeholder="Search" @update:model-value="applyFilter"/>
      </div>
    </template>
    <template #no-option>
      <div class="q-pa-sm">
        <q-input v-model="filter" dense outlined placeholder="Search" @update:model-value="applyFilter"/>
      </div>
      <q-item>
        <q-item-section class="text-italic text-grey">
          {{ not_found_label }}
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  option_value: {
    type: String,
    required: true,
  },
  option_label: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  not_found_label: {
    type: String,
    required: true,
  },
  default_value: {
    type: Object,
    required: false,
    default: null,
  },
  clearable: {
    type: Boolean,
    required: false,
    default: true,
  },
  required: {
    type: Boolean,
    required: false,
    default: false,
  },
})
const emit = defineEmits(['updateModel'])
function updateModel(model) {
  emit('updateModel', model)
}

const stringOptions = ref(props.options)
const model_default = ref(props.default_value)
const clearable = ref(props.clearable)
const model = ref(null)
const filter = ref('')

if (model_default.value !== null && model_default.value.id !== null)
  model.value = model_default.value

watch(() => props.options, (newOptions) => {
  stringOptions.value = newOptions
})

function filterFn(val, update) {
  if (val === '') {
    update(() => {
      stringOptions.value = props.options
    })
    return
  }
  update(() => {
    const needle = val.toLowerCase()
    stringOptions.value = props.options.filter(
      v => v.name.toLowerCase().includes(needle),
    )
  })
}

function applyFilter(value) {
  const val = filter.value
  const needle = val.toLowerCase()
  stringOptions.value = props.options.filter(
    v => v.name.toLowerCase().includes(needle),
  )
}
</script>