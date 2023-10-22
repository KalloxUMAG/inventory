<template>
  <div class="py-2 d-flex flex-row align-items-start">
    <div class="pr-2 pt-1">
      <p>{{ hour }}:00</p>
    </div>
    <div class="w-100">
      <hr />
      <div class="col p-0">
        <event-card
          v-for="(event, index) in events"
          :key="index"
          role="button"
          :event="event"
          :is-day-selected="true"
          @show-modal="(e) => emit('show-modal', e)"
          :is-list="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import EventCard from "./EventCard.vue";

const props = defineProps({
  hour: {
    type: String,
    required: false,
    default: "8",
  },
  events: {
    type: Array,
    required: false,
    default: () => [],
  },
});

const emit = defineEmits(["show-modal"]);
</script>
