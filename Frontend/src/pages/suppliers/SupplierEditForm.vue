<template>
    <PageTitle title="Nuevo proveedor" icon="add_business" />
    <q-form
      ref="createSupplierForm"
      class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
      @submit.prevent="onSubmit"
    >
      <FormSection title="Datos generales">
        <div class="row">
          <q-input
            v-model="supplier.name"
            outlined
            label="Nombre del proveedor*"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            v-model="supplier.rut"
            outlined
            label="Rut"
            mask="##.###.###-X"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            v-model="supplier.city_address"
            outlined
            label="Dirección*"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row">
          <q-input
            v-model="supplier.email"
            outlined
            label="Correo general*"
            class="col q-mr-md"
            type="email"
          />
        </div>
      </FormSection>
  
      <FormSection title="Contactos">
        <div v-for="(contact, index) in contacts" :key="index" class="row">
          <q-input
            v-model="contacts[index].name"
            outlined
            label="Nombre del contacto*"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <InputSelect
            outlined
            :default_value="{name: contacts[index].position, value: contacts[index].position}"
            :options="rolOptions"
            option_value="value"
            option_label="name"
            label="Roles"
            not_found_label="No hay roles disponibles"
            class="col q-mr-md"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="(value) => (contacts[index].position = value)"
          />
          <q-input
            v-model="contacts[index].phone"
            outlined
            label="Telefono trabajador"
            mask="(+##) #####-####"
            class="col q-mr-md"
          />
          <q-input
            v-model="contacts[index].email"
            outlined
            type="email"
            label="Correo trabajador"
            class="col q-mr-md"
          />
          <q-btn
            color="negative"
            class="q-mr-sm"
            size="md"
            icon="delete"
            flat
            @click="removeContact(index)"
          />
        </div>
        <div class="row">
          <q-btn
            class="add-btn q-mr-sm"
            icon="add"
            label="Agregar contacto"
            flat
            @click="addContact"
          />
        </div>
      </FormSection>
      <!-- Form button -->
      <div class="row justify-end q-mt-mx">
        <q-btn label="Guardar cambios" type="submit" color="positive" />
      </div>
      <q-inner-loading
        :showing="loading"
        label="Guardando cambios..."
        label-class="text-deep-orange"
        label-style="font-size: 1.6em"
      />
    </q-form>
    {{ id }}
  </template>
  
  <script setup>
  import { onMounted, reactive, ref, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { getSupplier, getSupplierContacts, postSupplierContact, updateSupplier, updateSupplierContact } from 'src/services'
  
  
  import PageTitle from 'src/components/commons/PageTitle.vue'
  import FormSection from 'src/components/form/FormSection.vue'
  import InputSelect from 'src/components/form/inputs/InputSelect.vue'
  
  const createSupplierForm = ref(null)
  const router = useRouter()
  const route = useRoute()

  const id = computed(() => route.params.id)

  
  const rolOptions = [
    {
      value: 'Vendedor',
      name: 'Vendedor',
    },
    {
      value: 'Tecnico',
      name: 'Tecnico',
    },
  ]
  
  const supplier = reactive({
    name: '',
    rut: '',
    city_address: '',
    email: '',
  })
  
  const contacts = ref([])
  
  const loading = ref(false)
  
  // Functions
  

  async function getSupplierData(){
    const supplierData = await getSupplier(id.value)
    supplier.name = supplierData.name
    supplier.rut = supplierData.rut
    supplier.city_address = supplierData.city_address
    supplier.email = supplierData.email

    const contactsData = await getSupplierContacts(id.value)
    contacts.value = contactsData
    
  }

  function addContact() {
    contacts.value.push({
      name: '',
      position: '',
      phone: '',
      email: '',
    })
  }
  
  function removeContact(index) {
    contacts.value.splice(index, 1)
  }
  
  async function onSubmit() {
    createSupplierForm.value.resetValidation()
    loading.value = true
    const supplierData = {
      name: supplier.name,
      rut: supplier.rut,
      city_address: supplier.city_address,
      contacts: contacts.value,
      email: supplier.email,
    }
    await updateSupplier(id.value, supplierData)
    contacts.value.forEach(async (contact) => {
      if (contact.supplier_id) {
        await updateSupplierContact(contact.id, contact)
      } else {
        contact.supplier_id = id.value
        await postSupplierContact(contact)
      }
    })
    loading.value = false
    router.push(`/suppliers/${id.value}`)
  }
  
  onMounted(() => {
    getSupplierData()
  })
  </script>
  
  <style scoped>
  .form-input {
    background-color: #fff;
    border: 1px solid #ced4da;
    border-radius: 12px;
    box-shadow: inset 0 1px 1px #00000013;
    color: #495057;
  }
  </style>
  