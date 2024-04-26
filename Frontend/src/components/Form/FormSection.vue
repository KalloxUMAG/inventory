<template>
    <div class="form-section__title">
        {{ title }}
    </div>
    <q-card class="my-card q-gutter-md col-12 q-pa-md gap-lg" flat bordered>
        <slot></slot>
    </q-card>
</template>

<script setup>
    const props = defineProps({
        title: String
    })
    const { title } = props
</script>

<style scoped>

.form-section__title {
    font-size: 1.5rem;
    font-weight: 500;
}

.my-card {
  width: 100%;
  border-radius: 12px !important;
}
</style>