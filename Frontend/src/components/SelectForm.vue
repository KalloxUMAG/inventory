<template>
  <q-select
    v-model="model"
    :options="stringOptions"
    :option-value="option_value"
    :option-label="option_label"
    emit-value
    map-options
    :label="label"
    @update:model-value="updateModel(model)"
    use-input
    input-debounce="0"
    @filter="filterFn"
    clearable
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">
          {{ not_found_label }}
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script setup>
import { onMounted, onUpdated, ref, watch } from "vue";

const emit = defineEmits(["updateModel"]);
function updateModel(model) {
  emit("updateModel", model);
}

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
});

const stringOptions = ref(props.options);
const model_default = ref(props.default_value);
const model = ref(model_default);
const filterFn = (val, update) => {
  if (val === "") {
    update(() => {
      stringOptions.value = props.options;
    });
    return;
  }
  update(() => {
    const needle = val.toLowerCase();
    stringOptions.value = props.options.filter(
      (v) => v.name.toLowerCase().indexOf(needle) > -1
    );
  });
};
/*
watch(props.options, (newOptions, oldOptions) => {
  if(oldOptions !== undefined){
    model.value = null;
    console.log("Value changed")
  }
  console.log("Updated")
})
*/
</script>
