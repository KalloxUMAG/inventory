<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent=""
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position"
        ref="createSupplyForm"
      >
      </q-form>
    </div>
  </q-page>
</template>

<script setup></script>

<style scoped>
body {
  background-image: url(./../assets/background.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

hr {
  width: 20%;
  height: 2px;
  background-color: black;
}

.q-form {
  margin-top: 10px;
  background-color: #fffffe;
  border-radius: 1%;
  border-width: 1px;
  border-style: solid;
}
</style>
