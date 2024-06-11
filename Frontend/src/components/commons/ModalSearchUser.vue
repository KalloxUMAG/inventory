<template>
  <div class="row">
    <q-dialog
      ref="serachUser"
      v-model="show"
      class="col-12 col-md-8 col-lg-6 col-xl-4"
      square
      transition-show
      @hide="emitCloseEvent"
    >
      <q-card>
        <q-card-section class="q-pa-lg">
          <h5 class="q-my-none text-bold">
            Buscar Usuarios
          </h5>
          <q-form class="row" @submit="submitForm" @reset="onReset">
            <q-input
              v-model="name"
              label="Nombre"
              class="col-12 col-md-6 q-pr-sm"
              :rules="[
                (val) =>
                  !!val
                  || !!email
                  || 'Debes ingresar al menos un nombre o email',
              ]"
            />
            <q-input
              v-model="email"
              label="Email"
              class="col-12 col-md-6"
              :rules="[
                (val) =>
                  !!val
                  || !!name
                  || 'Debes ingresar al menos un nombre o email',
              ]"
            />
            <div class="col-12 q-my-sm q-mt-lg">
              <q-btn
                label="Buscar"
                color="primary"
                icon-right="search"
                type="submit"
                size="lg"
                class="full-width"
              />
            </div>
          </q-form>

          <div>
            <h5 class="q-mb-sm">
              Seleccione un usuario
            </h5>
            <q-table
              v-model:selected="selectedUser"
              :rows="users"
              :columns="columns"
              row-key="email"
              no-data-label="No hay registros para mostrar"
              @row-click="
                (evt, row, index) => handleSelectedUser(evt, row, index)
              "
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, ref, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useUserStore } from 'stores'

const props = defineProps({
  showModalSearch: Boolean,
})
const emit = defineEmits(['close', 'selectedUser'])
const $q = useQuasar()
const userStore = useUserStore()

const name = ref('')
const email = ref('')
const users = ref([])
const selectedUser = ref([])
const show = ref(false)

function emitCloseEvent() {
  emit('close', false)
}

const columns = [
  {
    name: 'fullname',
    required: true,
    label: 'Nombre Completo',
    align: 'left',
    field: row => row.fullname,
  },
  {
    name: 'email',
    required: true,
    label: 'Email',
    align: 'left',
    field: row => row.email,
  },
]

watch(
  () => props.showModalSearch,
  (newVal) => {
    show.value = newVal
  },
)

async function submitForm() {
  try {
    const response = await userStore.fetchUser({
      fullname: name.value,
      email: email.value,
    })
    if (response && Array.isArray(response))
      users.value = response
    else
      users.value = []
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la marca: ${error}`,
    })
  }
}

function onReset() {
  name.value = ''
  email.value = ''
}

function handleSelectedUser(evt, row, index) {
  onReset()
  users.value = []

  emit('selectedUser', row)
}
</script>
