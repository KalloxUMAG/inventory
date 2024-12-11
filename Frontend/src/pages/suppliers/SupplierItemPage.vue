<template>
    <div v-if="supplier != null" class="col justify-center">
      <PageTitle :title="supplier.name" icon="store">
        <div>
          <q-btn
            outline
            color="secondary"
            label="Editar"
            @click=""
            disable
          />
        </div>
      </PageTitle>
  
      <div class="row q-col-gutter-md">
        <div class="col-12">
          <q-card class="bg-white no-shadow card_style" flat bordered>
            <q-card-section>
              <InfoSection
                title="Información general" :fields="[
                  {
                    label: 'Nombre',
                    value: supplier.name,
                  },
                  {
                    label: 'Rut',
                    value: supplier.rut,
                  },
                  {
                    label: 'Dirección',
                    value: supplier.city_address,
                  },
                  {
                    label: 'Correo general',
                    value: supplier.email,
                  },
                ]"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!--Contacts table-->
      <div class="q-mt-md col-12">
        <q-card class="no-shadow q-pa-xs card_style" flat bordered>
          <q-card-section class="q-pl-none">
            <div class="text-h5 text-weight-bold q-pl-md space-between">
              Contactos
              <div class="actions-buttons">
                <q-input
                  v-model="filter"
                  outlined
                  dense
                  debounce="300"
                  placeholder="Buscar"
                >
                  <template #append>
                    <q-icon name="search" />
                  </template>
                </q-input>
                <q-btn
                  class="add-btn q-mr-sm"
                  icon="add"
                  label="Agregar"
                  flat
                  @click=""
                  disable
                />
              </div>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-xs">
            <q-table
              :grid="$q.screen.xs"
              row-key="id"
              :columns="suppliersContactsColumns"
              :rows="contacts"
              no-data-label="No hay registros para mostrar"
              rows-per-page-label="Registros por pagina"
              flat
              bordered
              no-wrap
              :filter="filter"
              class="card-style"
            >
              <template #header="props">
                <q-tr :props="props">
                  <q-th
                    v-for="col in props.cols"
                    :key="col.name"
                    :props="props"
                    class="text-italic table-header"
                  >
                    {{ col.label }}
                  </q-th>
                </q-tr>
              </template>
              <template #body-cell="props">
                <q-td
                  :props="props"
                >
                  {{ props.value }}
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRoute, useRouter } from 'vue-router'
  import { computed, onMounted, ref } from 'vue'
  import PageTitle from 'src/components/commons/PageTitle.vue'
  import { useQuasar } from 'quasar'
  import { getSupplier, getSupplierContacts } from 'src/services'
  import {suppliersContactsColumns} from 'src/constants/columns'
  
  import InfoSection from 'src/components/item-page/InfoSection.vue'
  
  const $q = useQuasar()
  const router = useRouter()
  
  const content_loaded = ref(false)
  const filter = ref('')
  const supplier = ref(null)
  const contacts = ref([])
  
  const route = useRoute()
  const id = computed(() => route.params.id)
  
  async function getEquipmentData() {
    supplier.value = await getSupplier(id.value)
    contacts.value = await getSupplierContacts(id.value)
  }
  
  function editSupplier() {
    router.push(`/equipments/edit/${id.value}`)
  }
  
  onMounted(() => {
    getEquipmentData()
    content_loaded.value = true
  })
  </script>
  
  <style scoped>
  .item-title{
    align-content: center;
  }
  
  .card_style {
    border-radius: 12px;
  }
  
  .my-card {
    width: 100%;
    border-radius: 12px !important;
  }
  
  .container{
    border: 1px solid #d1d1d1 !important;
    border-radius: 12px !important;
    padding: 8px;
    overflow: visible;
  }
  
  .gap-lg{
    gap: 24px;
  }
  
  .image-visor{
    border: none !important;
    max-height: 500px;
    padding: 0;
  }
  
  .maintenance-table {
    width: 100%;
  }
  .field-label {
    font-size: 16px;
    font-weight: bold;
  }
  
  .field-content {
    font-size: 16px;
    font-weight: 500;
  }
  
  .card-style{
    border-radius: 12px;
  }
  .space-between{
    display: flex;
    justify-content: space-between;
  }
  .actions-buttons{
    display: inline-flex;
    gap: 10px;
    .add-btn{
      background-color: var(--add-btn-bg-color);
      color: var(--add-btn-text-color);
    }
  }
  </style>
  