<template>
    <div class="q-pa-md q-gutter-sm">
        <q-breadcrumbs active-color="secondary" class="text-dark">
            <q-breadcrumbs-el v-for="breadCrumb in breadCrumbs" :key="breadCrumb.text" :icon="breadCrumb.icon" :to="breadCrumb.to">
                <div class="breadcrumb-text">{{breadCrumb.text}}</div>
            </q-breadcrumbs-el>
        </q-breadcrumbs>
    </div>
</template>

<script setup>
    import {computed } from 'vue';
    import { useRouter } from 'vue-router';
    const route = useRouter();
    const breadCrumbs = computed(() => {
        if (typeof route.currentRoute.value.meta.breadCrumb === "function") {
            return route.currentRoute.value.meta.breadCrumb(route);
        }
        return route.currentRoute.value.meta.breadCrumb;
    })
</script>

<style>
.breadcrumb-text{
    padding-top: 2px;
}
.q-router-link--active:hover > .breadcrumb-text{
    text-decoration: underline;
}
</style>