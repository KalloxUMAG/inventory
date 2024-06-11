<template>
  <div class="panel no-margin" @click="showEventDetails">
    <div
      v-if="
        event?.isStarter
          && Object.values(selection).every((array) => array.length === 0)
      "
      class="alert event-title q-my-xs"
      :class="[getVariant(event?.status)]"
      role="alert"
    >
      <p class="no-margin">
        <span class="text-bold">Nombre :</span>
        {{ event?.supply.user_fullname }}
      </p>
      <p class="no-margin">
        <span class="text-bold">Equipo :</span>{{ event?.supply.equipment_name }}
      </p>
    </div>
    <div
      v-else-if="event?.showExtend"
      class="alert event-title"
      :class="[getVariant(event?.status)]"
      role="alert"
    >
      <p>
        <span class="text-bold">Nombre :</span>
        {{ event?.supply.user_fullname }}
      </p>
      <p class="no-margin">
        <span class="text-bold">Equipo :</span>
        {{ event?.supply.equipment_name }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, toRefs } from 'vue'

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
  selection: {
    type: Object,
    required: false,
    default: () => ({}),
  },
})

const emit = defineEmits(['show-modal'])

const { event, isDaySelected, isList } = toRefs(props)

function showEventDetails() {
  if (isDaySelected.value)
    emit('show-modal', event.value)
}

function getVariant(state) {
  switch (state) {
    case 1:
      return 'bg-grey-3'
    case 2:
      return 'bg-info'
    case 3:
      return 'bg-info'
    case 4:
      return 'bg-negative'
    case 5:
      return 'bg-warning'
    default:
      return 'bg-positive'
  }
}
</script>

<style scoped>
.event-title {
  padding: 0 5px;
  font-size: 12px;
}
</style>
