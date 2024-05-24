<template>
  <PageTitle title="Nuevo equipamiento" />
  <q-form
    ref="createEquipmentForm"
    class="q-gutter-md col-xs-12 col-sm-12 col-md-6 relative-position q-mr-md"
    @submit.prevent="onSubmit"
    @reset="onReset"
  >
    <!-- Datos Producto -->
    <FormSection title="Datos equipo">
      <q-input
        v-model="name"
        outlined
        maxlength="49"
        label="Nombre del equipo*"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Este campo es obligatorio',
          (val) =>
            (val && val.length < 50)
            || 'El nombre debe contener menos de 50 caracteres',
        ]"
      />
      <q-input
        v-model="serial"
        outlined
        maxlength="30"
        label="Código serial*"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Este campo es obligatorio',
          (val) => (val && val.length < 256) || 'Máximo 255 caracteres',
        ]"
      />
      <q-input
        v-model="inventory"
        outlined
        maxlength="11"
        type="number"
        label="Inventario UMAG*"
        lazy-rules
        :rules="[
          (val) =>
            (val.length < 26 && val > 0)
            || 'El valor debe ser mayor que 0 y tener un maximo de 25 dígitos',
        ]"
      />

      <!-- Brand Model Number -->

      <div class="row justify-center">
        <div v-if="!newbrandstate" class="col q-mr-md">
          <SelectForm
            outlined
            class="row q-mr-md"
            :disable="disableBrand"
            :options="brandOptions"
            option_value="id"
            option_label="name"
            label="Marca"
            not_found_label="No hay marcas disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                brand = value;
                getModelsData();
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir marca"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="newbrandstate = !newbrandstate"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="newbrand"
              outlined
              label="Nombre marca"
              class="col"
              :disable="disableBrand"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="!newbrandstate && !newmodelstate" class="col q-mr-md">
          <SelectForm
            outlined
            class="row q-mr-md"
            :disable="disableBrand"
            :options="modelOptions"
            option_value="id"
            option_label="name"
            label="Modelo"
            not_found_label="No hay modelos disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                model = value;
                getModelNumbersData();
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir modelo"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="newmodelstate = !newmodelstate"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="newmodel"
              outlined
              label="Nombre modelo"
              class="col"
              :disable="disableBrand"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div
          v-if="!newbrandstate && !newmodelstate && !newmodelnumberstate"
          class="col"
        >
          <SelectForm
            outlined
            class="row"
            :disable="disableBrand"
            :options="modelNumberOptions"
            option_value="id"
            option_label="name"
            label="Número modelo"
            not_found_label="No hay número de modelo disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                modelNumber = value;
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir nro. modelo"
              icon="add"
              class="add-btn text-caption"
              @click="newmodelnumberstate = !newmodelnumberstate"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="newmodelnumber"
              outlined
              label="Número modelo"
              class="col"
              :disable="disableBrand"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
      </div>
      <div
        v-if="newmodelstate || newmodelnumberstate || newbrandstate"
        class="row justify-end q-pt-md"
      >
        <q-btn
          v-if="disableBrand"
          label="Editar"
          color="amber"
          class="q-mr-sm"
          @click="disableBrand = false"
        />
        <q-btn
          v-else
          label="Guardar"
          color="amber"
          class="q-mr-sm"
          @click="disableBrand = true"
        />
        <q-btn
          label="Ver lista"
          color="amber"
          @click="
            (newmodelnumberstate = false),
            (newmodelstate = false),
            (newbrandstate = false),
            (disableBrand = false)
          "
        />
      </div>

      <!-- Mantenimiento -->
      <q-checkbox
        v-model="maintenanceApply"
        val="lg"
        label="Aplica para mantención"
      />
      <SelectForm
        v-if="maintenanceApply"
        outlined
        :options="maintenanceOptions"
        option_value="value"
        option_label="name"
        label="Periodo de mantención"
        not_found_label="No hay periodos disponibles"
        :rules="[(val) => !!val || 'Campo obligatorio']"
        lazy-rules
        @update-model="(value) => (maintenance = value)"
      />
      <!-- Observacion -->
      <q-input
        v-model="observation"
        outlined
        type="textarea"
        label="Observación"
        :rules="[(val) => !!val || 'Campo obligatorio']"
        lazy-rules
      />

      <!-- Imagenes equipamiento equipmentImages -->
      <div class="row">
        <div class="col">
          <UploadImages
            label="Imagenes equipamiento"
            :max_files="5"
            :handle-add-images="handleAddImages"
            :handle-remove-images="handleRemoveImages"
          />
        </div>
      </div>
    </FormSection>
    <!-- Datos de compra -->
    <FormSection title="Datos compra">
      <!-- Datos de proveedor -->
      <SelectForm
        outlined
        :options="suppliersOptions"
        option_value="id"
        option_label="name"
        label="Proveedor"
        not_found_label="No hay proveedores disponibles"
        :rules="[
          /*[val => !!val || 'Campo obligatorio']*/
        ]"
        lazy-rules
        @update-model="
          (value) => {
            (supplier = value), getInvoicesSupplierData(value);
          }
        "
      />

      <q-input
        v-model="reception_date"
        outlined
        label="Fecha de recepción"
        stack-label
        lazy-rules
        :rules="[
          /*(val) => (val && val != null) || 'Este campo es obligatorio',*/
        ]"
      >
        <template #append>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-date v-model="reception_date" mask="YYYY-MM-DD">
                <div class="row items-center justify-end">
                  <q-btn v-close-popup label="Close" color="primary" flat />
                </div>
              </q-date>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>

      <!-- Invoices -->
      <div v-if="!newinvoicestate">
        <SelectForm
          outlined
          :options="invoicesOptions"
          option_value="id"
          option_label="name"
          label="Facturas"
          not_found_label="No hay facturas disponibles"
          :rules="[
            /*val => !!val || 'Campo obligatorio'*/
          ]"
          lazy-rules
          @update-model="(value) => (invoice = value)"
        />
        <div class="row justify-end q-mt-md">
          <q-btn
            label="Añadir factura"
            icon="add"
            class="add-btn text-caption"
            @click="newinvoicestate = !newinvoicestate"
          />
        </div>
      </div>

      <div v-else>
        <div class="row">
          <q-input
            v-model="newinvoicenumber"
            outlined
            label="Numero"
            type="number"
            class="col"
            :disable="disableInvoice"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <q-input
            v-model="newinvoicedate"
            outlined
            label="Fecha"
            type="date"
            stack-label
            class="col q-ml-md"
            :disable="disableInvoice"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
        </div>
        <div class="row q-mt-sm">
          <q-file
            v-model="invoiceimage"
            outlined
            class="col"
            label="Foto de factura"
            accept=".jpg, image/*"
            :disable="disableInvoice"
            clearable
          >
            <template #prepend>
              <q-icon name="cloud_upload" />
            </template>
          </q-file>
        </div>
        <div class="row justify-end q-mt-sm">
          <q-btn
            v-if="disableInvoice"
            label="Editar"
            color="amber"
            class="q-mr-sm"
            @click="disableInvoice = false"
          />
          <q-btn
            v-else
            label="Guardar"
            color="amber"
            class="q-mr-sm"
            @click="disableInvoice = true"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="
              (newinvoicestate = !newinvoicestate), (disableInvoice = false)
            "
          />
        </div>
      </div>

      <!-- Projects stages and owner -->

      <div class="row justify-center">
        <div v-if="!newprojectstate" class="col q-mr-md">
          <SelectForm
            outlined
            class="row q-mr-md"
            :disable="disableProject"
            :options="projectOptions"
            option_value="id"
            option_label="name"
            label="Proyectos"
            not_found_label="No hay proyectos disponibles"
            :rules="[
              /*val => !!val || 'Campo obligatorio'*/
            ]"
            lazy-rules
            @update-model="
              (value) => {
                project = value;
                getStagesData();
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Proyecto"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="newprojectstate = !newprojectstate"
            />
          </div>
        </div>
        <div v-else class="col q-mr-lg">
          <div class="row">
            <q-input
              v-model="newprojectname"
              outlined
              label="Nombre proyeto"
              class="col"
              :disable="disableProject"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>

        <div v-if="!newstagestate && !newprojectstate" class="col q-ml-md">
          <SelectForm
            outlined
            class="row"
            :disable="disableProject"
            :options="stagesOptions"
            option_value="id"
            option_label="name"
            label="Etapas"
            not_found_label="No hay etapas disponibles"
            :rules="[
              /*val => !!val || 'Campo obligatorio'*/
            ]"
            lazy-rules
            @update-model="(value) => (stage = value)"
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Etapa"
              icon="add"
              class="add-btn text-caption q-ml-md"
              @click="newstagestate = !newstagestate"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="newstagename"
              outlined
              label="Nombre etapa"
              class="col"
              :disable="disableProject"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
      </div>
      <div v-if="newstagestate || newprojectstate" class="row justify-end">
        <q-btn
          v-if="disableProject"
          label="Editar"
          color="amber"
          class="q-mr-sm"
          @click="disableProject = false"
        />
        <q-btn
          v-else
          label="Guardar"
          color="amber"
          class="q-mr-sm"
          @click="disableProject = true"
        />
        <q-btn
          label="Ver lista"
          color="amber"
          @click="
            (newstagestate = false),
            (newprojectstate = false),
            (disableProject = false)
          "
        />
      </div>
      <div v-if="newprojectstate" class="row">
        <div v-if="!newProjectOwnerState" class="col">
          <SelectForm
            outlined
            class="row"
            :disable="disableProjectOwner"
            :options="projectOwnersOptions"
            option_value="id"
            option_label="name"
            label="Dueño proyecto"
            not_found_label="No hay dueños disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                projectowner = value;
              }
            "
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir dueño"
              color="amber"
              class="add-btn"
              @click="newProjectOwnerState = true"
            />
          </div>
        </div>
        <div v-else class="col">
          <q-input
            v-model="newprojectownername"
            outlined
            class="row"
            label="Nombre dueño"
            :disable="disableProjectOwner"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              v-if="disableProjectOwner"
              label="Editar"
              color="amber"
              class="q-mr-sm"
              @click="disableProjectOwner = false"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              class="q-mr-sm"
              @click="disableProjectOwner = true"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (disableProjectOwner = false), (newProjectOwnerState = false)
              "
            />
          </div>
        </div>
      </div>
    </FormSection>
    <!-- Location -->
    <FormSection title="Datos ubicación">
      <div class="row justify-center">
        <div v-if="!newbuildingstate" class="col q-mr-md">
          <SelectForm
            outlined
            class="row q-mr-md"
            :disable="disableLocation"
            :options="buildingOptions"
            option_value="id"
            option_label="name"
            label="Edificio"
            not_found_label="No hay edificios disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                building = value;
                getUnitsData();
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Edificio"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="newbuildingstate = !newbuildingstate"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="newbuildingname"
              outlined
              label="Nombre edificio"
              class="col"
              :disable="disableLocation"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="!newbuildingstate && !newunitstate" class="col q-mr-md">
          <SelectForm
            outlined
            class="row q-mr-md"
            :disable="disableLocation"
            :options="unitOptions"
            option_value="id"
            option_label="name"
            label="Unidad"
            not_found_label="No hay una unidad disponible"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                unit = value;
                getRoomsData();
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              outlined
              label="Añadir unidad"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="newunitstate = !newunitstate"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="newunitname"
              outlined
              label="Nombre unidad"
              class="col"
              :disable="disableLocation"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div
          v-if="!newbuildingstate && !newunitstate && !newroomstate"
          class="col"
        >
          <SelectForm
            outlined
            class="row"
            :disable="disableLocation"
            :options="roomOptions"
            option_value="id"
            option_label="name"
            label="Sala"
            not_found_label="No hay salas disponibles"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
            @update-model="
              (value) => {
                room = value;
              }
            "
          />
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir sala"
              icon="add"
              class="add-btn text-caption"
              @click="newroomstate = !newroomstate"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="newroomname"
              outlined
              label="Nombre sala"
              class="col"
              :disable="disableLocation"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
      </div>
      <div
        v-if="newbuildingstate || newunitstate || newroomstate"
        class="row justify-end"
      >
        <q-btn
          v-if="disableLocation"
          label="Editar"
          color="amber"
          class="q-mr-sm"
          @click="disableLocation = false"
        />
        <q-btn
          v-else
          label="Guardar"
          color="amber"
          class="q-mr-sm"
          @click="disableLocation = true"
        />
        <q-btn
          label="Ver lista"
          color="amber"
          @click="
            (newbuildingstate = false),
            (newunitstate = false),
            (newroomstate = false),
            (disableLocation = false)
          "
        />
      </div>
    </FormSection>
    <!-- Form button -->
    <div class="row justify-end q-mt-mx">
      <q-btn label="Crear" type="submit" color="positive" />
    </div>
    <q-inner-loading
      :showing="loading"
      label="Creando equipamiento"
      label-class="text-deep-orange"
      label-style="font-size: 1.6em"
    />
  </q-form>
</template>

<script setup>
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { sendRequest } from 'src/services/axios/instance.js'

import { getBrands, getBuildings, getInvoices, getInvoicesSupplier, getModelNumbers, getModels, getProjectOwners, getProjects, getRooms, getStages, getSuppliers, getUnits } from '/src/services'

import SelectForm from 'src/components/SelectForm.vue'
import UploadImages from 'src/components/UploadImages.vue'
import FormSection from 'src/components/Form/FormSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

const maintenanceOptions = [
  {
    value: 1,
    name: 'Mensual',
  },
  {
    value: 3,
    name: 'Trimestral',
  },
  {
    value: 6,
    name: 'Semestral',
  },
  {
    value: 12,
    name: 'Anual',
  },
]

const brand = ref(null)
const brandOptions = ref([])
const building = ref(null)
const buildingOptions = ref([])
const createEquipmentForm = ref(null)
const disableBrand = ref(false)
const disableInvoice = ref(false)
const disableLocation = ref(false)
const disableProject = ref(false)
const disableProjectOwner = ref(false)
const equipmentimages = ref([])
const invoiceimage = ref(null)
const name = ref(null)
const serial = ref(null)
const inventory = ref(0)
const invoice = ref(null)
const invoicesOptions = ref([])
const loading = ref(false)
const model = ref(null)
const modelOptions = ref([])
const modelNumber = ref(null)
const modelNumberOptions = ref([])
const maintenance = ref(null)
const observation = ref(null)
const newbrandstate = ref(false)
const newbuildingname = ref(null)
const newbuildingstate = ref(false)
const newinvoicestate = ref(false)
const newmodelstate = ref(null)
const newmodelnumberstate = ref(false)
const newmodel = ref(null)
const newmodelnumber = ref(null)
const newbrand = ref(null)
const newinvoicenumber = ref(null)
const newinvoicedate = ref(null)
const newprojectstate = ref(null)
const newprojectname = ref(null)
const newProjectOwnerState = ref(false)
const newprojectownername = ref(null)
const newroomname = ref(null)
const newroomstate = ref(null)
const newstagestate = ref(null)
const newstagename = ref(null)
const newsupplierstate = ref(false)
const newsuppliername = ref(null)
const newsupplierrut = ref(null)
const newsupplieraddress = ref(null)
const newunitname = ref(null)
const newunitstate = ref(false)
const project = ref(null)
const projectowner = ref(null)
const projectOptions = ref([])
const projectOwnersOptions = ref([])
const reception_date = ref(null)
const stage = ref(null)
const stagesOptions = ref([])
const room = ref(null)
const roomOptions = ref([])
const maintenanceApply = ref(false)
const supplier = ref(null)
const suppliersOptions = ref([])
const unit = ref(null)
const unitOptions = ref([])
const workername1 = ref(null)
const workerrol1 = ref(null)
const workermail1 = ref(null)
const workerphone1 = ref(null)
const workername2 = ref(null)
const workerrol2 = ref(null)
const workermail2 = ref(null)
const workerphone2 = ref(null)
const $q = useQuasar()
const router = useRouter()
const api_prefix = process.env.API_URL

function handleAddImages(files) {
  equipmentimages.value.push(files[0])
}

function handleRemoveImages(files) {
  equipmentimages.value = equipmentimages.value.filter((value) => {
    return value !== files[0]
  })
}

async function getBrandsData() {
  const brands = await getBrands()
  brandOptions.value = brands.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getBuildingsData() {
  const buildings = await getBuildings()
  buildingOptions.value = buildings.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getInvoicesData() {
  const invoices = await getInvoices()
  invoicesOptions.value = invoices.map((x) => {
    return { id: x.id, name: x.number.toString() }
  })
}

async function getInvoicesSupplierData(supplier_id) {
  const invoices = await getInvoicesSupplier(supplier_id)
  invoicesOptions.value = invoices.map((x) => {
    return { id: x.id, name: x.number.toString() }
  })
}

async function getModelsData() {
  const models = await getModels(brand.value)
  modelOptions.value = models.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getModelNumbersData() {
  const modelnumbers = getModelNumbers(model.value)
  modelNumberOptions.value = modelnumbers.map((x) => {
    return { id: x.id, name: x.number }
  })
}

async function getProjectsData() {
  const projects = await getProjects()
  projectOptions.value = projects.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getProjectOwnersData() {
  const projectsowners = await getProjectOwners()
  projectOwnersOptions.value = projectsowners.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getRoomsData() {
  const rooms = await getRooms(unit.value)
  room.value = null
  roomOptions.value = rooms.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getStagesData() {
  const stages = await getStages(project.value)
  stage.value = null
  stagesOptions.value = stages.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getSuppliersData() {
  const suppliers = await getSuppliers()
  suppliersOptions.value = suppliers.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getUnitsData() {
  const units = await getUnits(building.value)
  unit.value = null
  room.value = null
  roomOptions.value = []
  unitOptions.value = units.map((x) => {
    return { id: x.id, name: x.name }
  })
}

function onReset() {
  name.value = null
  serial.value = null
  inventory.value = null
  model.value = null
  maintenance.value = null
  observation.value = null
  reception_date.value = null
}

async function createNewBrand() {
  if (!newbrandstate.value)
    return brand.value

  const branddata = {
    name: newbrand.value,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/brands`,
      data: branddata,
    })
    return response.data
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

async function createNewBuilding() {
  if (!newbuildingstate.value)
    return building.value

  const buildingdata = {
    name: newbuildingname.value,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/buildings`,
      data: buildingdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el edificio: ${error}`,
    })
  }
}

async function createNewInvoice(supplier_id) {
  if (!newinvoicestate.value)
    return invoice.value

  const invoicedata = {
    number: newinvoicenumber.value,
    date: newinvoicedate.value,
    supplier_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/invoices`,
      data: invoicedata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la factura: ${error}`,
    })
  }
}

async function createNewModel(brand_id) {
  if (!newbrandstate.value && !newmodelstate.value)
    return model.value

  const newmodeldata = {
    name: newmodel.value,
    brand_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/models`,
      data: newmodeldata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el modelo: ${error}`,
    })
    return -1
  }
}

async function createNewModelnumber(model_id) {
  if (!newbrandstate.value && !newmodelstate.value && !newmodelnumber.value)
    return modelNumber.value

  const newmodelnumberdata = {
    number: newmodelnumber.value,
    model_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/model_numbers`,
      data: newmodelnumberdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el número de modelo: ${error}`,
    })
  }
}

async function createNewProject(project_owner_id) {
  if (!newprojectstate.value)
    return project.value

  const projectname = newprojectname.value

  if (projectname.trim().length === 0)
    return -1

  if (project_owner_id === -1)
    project_owner_id = null

  const projectdata = {
    name: projectname,
    owner_id: project_owner_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/projects`,
      data: projectdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el proyecto: ${error}`,
    })
  }
}

async function createNewProjectOwner() {
  if (!newProjectOwnerState.value)
    return projectowner.value

  const projectownername = newprojectownername.value

  if (projectownername.trim().length === 0)
    return -1

  const projectownerdata = {
    name: projectownername,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/project_owners`,
      data: projectownerdata,
    })
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el dueño: ${error}`,
    })
  }
}

async function createNewUnit(building_id) {
  if (!newbuildingstate.value && !newunitstate.value)
    return unit.value

  const unitdata = {
    name: newunitname.value,
    building_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/units`,
      data: unitdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la unidad: ${error}`,
    })
  }
}

async function createNewRoom(unit_id) {
  if (!newbuildingstate.value && !newunitstate.value && !newroomstate.value)
    return room.value

  const roomdata = {
    name: newroomname.value,
    unit_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/rooms`,
      data: roomdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la sala: ${error}`,
    })
  }
}

async function createNewSupplier() {
  if (!newsupplierstate.value)
    return supplier.value

  const supplierdata = {
    name: newsuppliername.value,
    rut: newsupplierrut.value,
    city_address: newsupplieraddress.value,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/suppliers`,
      data: supplierdata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el proveedor: ${error}`,
    })
  }
}

async function createNewWorker(supplier_id) {
  if (!newsupplierstate.value)
    return

  if (workername1.value != null) {
    const workerdata1 = {
      name: workername1.value,
      position: workerrol1.value,
      phone: workerphone1.value,
      email: workermail1.value,
      supplier_id,
    }

    try {
      const response = await sendRequest({
        method: 'POST',
        url: `${api_prefix}/suppliers_contacts`,
        data: workerdata1,
      })
    }
    catch (error) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `No se pudo crear el contacto 1: ${error}`,
      })
    }
  }
  if (workername2.value != null) {
    const workerdata2 = {
      name: workername2.value,
      position: workerrol2.value,
      phone: workerphone2.value,
      email: workermail2.value,
      supplier_id,
    }
    try {
      const response = await sendRequest({
        method: 'POST',
        url: `${api_prefix}/suppliers_contacts`,
        data: workerdata2,
      })
    }
    catch (error) {
      $q.notify({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: `No se pudo crear el contacto 2: ${error}`,
      })
    }
  }
}

async function createNewStage(project_id) {
  if (!newstagestate.value && !newprojectstate.value)
    return stage.value

  const stagename = newstagename.value

  if (stagename.trim().length === 0)
    return -1

  const stagedata = {
    name: newstagename.value,
    project_id,
  }

  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/stages`,
      data: stagedata,
    })
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear la etapa: ${error}`,
    })
  }
}

async function createNewEquipment(equipmentdata) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/equipments`,
      data: equipmentdata,
    })
    if (response.status === 201) {
      $q.notify({
        color: 'green-4',
        textColor: 'white',
        icon: 'check',
        message: 'Equipo creado con éxito',
      })
    }
    return response.data
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo crear el equipo: ${error}`,
    })
  }
}

async function uploadInvoiceImage(equipment_id) {
  if (!newinvoicestate.value || invoiceimage.value == null)
    return

  const formData = new FormData()
  formData.append('file', invoiceimage.value)
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/invoices${equipment_id}`,
      data: formData,
    })
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo guardar la imagen de factura: ${error}`,
    })
  }
}

async function uploadEquipmentImage(equipment_id) {
  if (equipmentimages.value == null)
    return

  equipmentimages.value.forEach((image) => {
    const formData = new FormData()
    formData.append('file', image)
    uploadEquipmentImage2(equipment_id, formData)
  })
}

async function uploadEquipmentImage2(equipment_id, formData) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/equipments/${equipment_id}`,
      data: formData,
    })
  }
  catch (error) {
    $q.notify({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: `No se pudo guardar la imagen del equipo: ${error}`,
    })
  }
}

async function onSubmit() {
  createEquipmentForm.value.resetValidation()
  const equipmentdata = {
    name: name.value,
    serial_number: serial.value,
    umag_inventory_code: inventory.value,
    reception_date: reception_date.value,
    observation: observation.value,
    model_number_id: modelNumber.value,
    supplier_id: supplier.value,
    invoice_id: invoice.value,
    room_id: room.value,
    stage_id: stage.value,
    last_preventive_mainteinance: reception_date.value,
  }
  loading.value = true
  if (maintenanceApply.value)
    equipmentdata.maintenance_period = maintenance.value

  const building_id = await createNewBuilding()
  if (building_id === -1) {
    loading.value = false
    return
  }
  const unit_id = await createNewUnit(building_id)
  if (unit_id === -1) {
    loading.value = false
    return
  }
  const room_id = await createNewRoom(unit_id)
  if (room_id === -1) {
    loading.value = false
    return
  }
  equipmentdata.room_id = room_id

  const brand_id = await createNewBrand()
  if (brand_id === -1) {
    loading.value = false
    return
  }
  const model_id = await createNewModel(brand_id)
  if (model_id === -1) {
    loading.value = false
    return
  }
  const model_number_id = await createNewModelnumber(model_id)
  if (model_number_id === -1) {
    loading.value = false
    return
  }

  equipmentdata.model_number_id = model_number_id

  const supplier_id = await createNewSupplier()
  if (supplier_id === -1) {
    loading.value = false
    return
  }
  equipmentdata.supplier_id = supplier_id
  await createNewWorker(supplier_id)
  const invoice_id = await createNewInvoice(supplier_id)
  if (invoice_id === -1) {
    loading.value = false
    return
  }
  equipmentdata.invoice_id = invoice_id

  const project_owner_id = await createNewProjectOwner()
  const project_id = await createNewProject(project_owner_id)
  const stage_id = await createNewStage(project_id)
  if (stage_id === -1) {
    loading.value = false
    return
  }
  equipmentdata.stage_id = stage_id
  const equipment_id = await createNewEquipment(equipmentdata)
  await uploadEquipmentImage(equipment_id)
  await uploadInvoiceImage(equipment_id)
  loading.value = false
  // onReset()

  redirectToEquipment(equipment_id.toString())
}

function redirectToEquipment(equipment_id) {
  router.push({ path: equipment_id })
}

onMounted(() => {
  getBrandsData()
  getInvoicesData()
  getProjectsData()
  getProjectOwnersData()
  getSuppliersData()
  getBuildingsData()
})
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.add-btn {
  background-color: #7b7bd2 !important;
  color: #fff;
  border: 2px solid #7777cf;
}

.section-title {
  text-align: center;
  font-weight: bold;
  font-size: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

hr {
  width: 20%;
  height: 2px;
  background-color: black;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>
