<template>
  <PageTitle title="Nuevo Grupo" icon="group"/>
    <div class="row justify-center">
    <q-form
      @submit.prevent="onSubmit"
      @reset="onReset"
      class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
      ref="createEquipmentForm"
    >
    <!--Form button-->
    <div class="row justify-end q-mt-mx">
        <q-btn label="Crear" type="submit" color="positive" />
      </div>
    </q-form>
  </div>
</template>

<script setup>
    import PageTitle from 'src/components/commons/PageTitle.vue';
</script>