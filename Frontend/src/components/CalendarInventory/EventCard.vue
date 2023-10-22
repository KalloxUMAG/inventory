<template>
  <div class="panel no-margin" @click="showEventDetails">
    <div
      class="alert event-title"
      :class="[getVariant(event?.status)]"
      role="alert"
    >
      <p class="no-margin">Insumo : {{ event?.supply.consumables.label }}</p>
      <p>Rut : {{ event?.supply.dni }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, defineEmits, toRefs } from "vue";

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
  isDaySelected: {
    type: Boolean,
  },
  isList: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["show-modal"]);

const { event, isDaySelected, isList } = toRefs(props);

const showEventDetails = () => {
  if (isDaySelected.value) {
    emit("show-modal", event.value);
  }
};

const getVariant = (state) => {
  switch (state) {
    case 1:
      return "bg-grey-3";
    case 2:
      return "bg-info";
    case 3:
      return "bg-positive";
    case 4:
      return "bg-negative";
    case 5:
      return "bg-warning";
    default:
      return "bg-info";
  }
};
</script>

<style scoped>
.event-title {
  padding: 0 5px;
  font-size: 12px;
}
</style>
