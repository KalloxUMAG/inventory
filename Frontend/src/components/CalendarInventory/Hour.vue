<template>
  <div class="py-2 d-flex flex-row align-items-start">
    <div class="pr-2 pt-1">
      <p>{{ hour }}:00</p>
    </div>
    <div class="w-100">
      <hr>
      <div class="col p-0">
        <EventCard
          v-for="(event, index) in events"
          :key="index"
          role="button"
          :event="event"
          :is-day-selected="true"
          :is-list="true"
          @show-modal="(e) => emit('show-modal', e)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue'
import EventCard from './EventCard.vue'

const props = defineProps({
  hour: {
    type: String,
    required: false,
    default: '8',
  },
  events: {
    type: Array,
    required: false,
    default: () => [],
  },
})

const emit = defineEmits(['show-modal'])
</script>
