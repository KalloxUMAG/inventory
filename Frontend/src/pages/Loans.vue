<template>
  <div class="row q-pa-md">
    <section class="col-12">
      <div class="row justify-between items-center">
        <PageTitle title="Prestamos" icon="calendar_month" />
        <div>
          <div v-if="showModal">
            <eventModal
              :show-modal="showModal"
              :event="event"
              :title="event?.title ?? 'Suministrar insumo'"
              @create="AddSupply"
              @close="hideModal"
            />
          </div>
        </div>
      </div>
    </section>
    <div class="col-12 row justify-end q-my-md">
      <div class="q-mr-md">
        <q-btn
          size="12px"
          color="white"
          text-color="primary"
          label="Agregar"
          @click="AddLoan"
        />
      </div>
    </div>
    <div class="col-12 row">
      Contenido
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import PageTitle from 'src/components/commons/PageTitle.vue'
import { useQuasar } from 'quasar'
import dayjs from 'dayjs'
import eventModal from '../components/Loans/LoanFormModal.vue'

dayjs.locale('es')

const $q = useQuasar()

const event = ref(null)
const showModal = ref(false)

async function AddLoan() {
  $q.dialog({
    component: eventModal,
  }).onOk((data) => {
    console.log('Ok')
  })
}

onMounted(() => {
})
</script>
