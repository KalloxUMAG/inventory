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
        <div v-if="!brand.newBrandState" class="col q-mr-md">
          <div v-if="brand.default">
            <SelectForm
              outlined
              class="row q-mr-md"
              :disable="brand.disable"
              :default_value="brand.default"
              :options="brandOptions"
              option_value="id"
              option_label="name"
              label="Marca"
              not_found_label="No hay marcas disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  brand.model = value;
                  brand.name = value ? brandOptions.find((x) => x.id === value).name : null;
                  getModelsData();
                }
              "
            />
          </div>

          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir marca"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="brand.newBrandState = !brand.newBrandState"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="brand.newBrand"
              outlined
              label="Nombre marca"
              class="col"
              :disable="brand.disable"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="!brand.newBrandState && !model.newModelState" class="col q-mr-md">
          <div v-if="model.default">
            <SelectForm
              outlined
              class="row q-mr-md"
              :default_value="model.default"
              :disable="brand.disable"
              :options="modelOptions"
              option_value="id"
              option_label="name"
              label="Modelo"
              not_found_label="No hay modelos disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  model.model = value;
                  model.name = value ? modelOptions.find((x) => x.id === value).name : null;
                  getModelNumbersData();
                }
              "
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir modelo"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="model.newModelState = !model.newModelState"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="model.newModel"
              outlined
              label="Nombre modelo"
              class="col"
              :disable="brand.disable"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div
          v-if="!brand.newBrandState && !model.newModelState && !modelNumber.newModelNumberState"
          class="col"
        >
          <div v-if="modelNumber.default">
            <SelectForm
              outlined
              class="row"
              :default_value="modelNumber.default"
              :disable="brand.disable"
              :options="modelNumberOptions"
              option_value="id"
              option_label="name"
              label="Número modelo"
              not_found_label="No hay número de modelo disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  modelNumber.model = value;
                  modelNumber.name = value ? modelNumberOptions.find((x) => x.id === value).name : null;
                }
              "
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir nro. modelo"
              icon="add"
              class="add-btn text-caption"
              @click="modelNumber.newModelNumberState = !modelNumber.newModelNumberState"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="modelNumber.newModelNumber"
              outlined
              label="Número modelo"
              class="col"
              :disable="brand.disable"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
      </div>
      <div
        v-if="model.newModelState || modelNumber.newModelNumberState || brand.newBrandState"
        class="row justify-end q-pt-md"
      >
        <q-btn
          v-if="brand.disable"
          label="Editar"
          color="amber"
          class="q-mr-sm"
          @click="brand.disable = false"
        />
        <q-btn
          v-else
          label="Guardar"
          color="amber"
          class="q-mr-sm"
          @click="brand.disable = true"
        />
        <q-btn
          label="Ver lista"
          color="amber"
          @click="
            (modelNumber.newModelNumberState = false),
            (model.newModelState = false),
            (brand.newBrandState = false),
            (brand.disable = false)
          "
        />
      </div>

      <!-- Mantenimiento -->
      <q-checkbox
        v-model="maintenance.apply"
        val="lg"
        label="Aplica para mantención"
      />
      <div v-if="maintenance.default">
        <SelectForm
          v-if="maintenance.apply"
          outlined
          :default_value="maintenance.default"
          :options="maintenanceOptions"
          option_value="id"
          option_label="name"
          label="Periodo de mantención"
          not_found_label="No hay periodos disponibles"
          :rules="[(val) => !!val || 'Campo obligatorio']"
          lazy-rules
          @update-model="(value) => { maintenance.model = value; maintenance.name = maintenanceOptions.find((x) => x.id === value).name }"
        />
      </div>

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
        <UploadImages
          ref="uploaderComponent"
          label="Imagenes equipamiento"
          :max_files="5"
          :handle-add-images="handleAddImages"
          :handle-remove-images="handleRemoveImages"
        />
      </div>
    </FormSection>
    <!-- Datos de compra -->
    <FormSection title="Datos compra">
      <!-- Datos de proveedor -->
      <div>
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
        <div class="row justify-end q-mt-md">
          <q-btn
            label="Añadir proveedor"
            icon="add"
            class="add-btn text-caption"
            @click="newSupplier"
          />
        </div>
      </div>

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
      <div v-if="!invoice.newInvoiceState">
        <SelectForm
          outlined
          :default_value="invoice.default"
          :options="invoicesOptions"
          option_value="id"
          option_label="name"
          label="Facturas"
          not_found_label="No hay facturas disponibles"
          :rules="[
            /*val => !!val || 'Campo obligatorio'*/
          ]"
          lazy-rules
          @update-model="(value) => {
            invoice.model = value;
            invoice.name = invoicesOptions.find((x) => x.id === value).name;
          }"
        />
        <div class="row justify-end q-mt-md">
          <q-btn
            label="Añadir factura"
            icon="add"
            class="add-btn text-caption"
            @click="invoice.newInvoiceState = !invoice.newInvoiceState"
          />
        </div>
      </div>

      <div v-else>
        <div class="row">
          <q-input
            v-model="invoice.newInvoiceNumber"
            outlined
            label="Numero"
            type="number"
            class="col"
            :disable="invoice.disable"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <q-input
            v-model="invoice.newInvoiceDate"
            outlined
            label="Fecha"
            type="date"
            stack-label
            class="col q-ml-md"
            :disable="invoice.disable"
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
            :disable="invoice.disable"
            clearable
          >
            <template #prepend>
              <q-icon name="cloud_upload" />
            </template>
          </q-file>
        </div>
        <div class="row justify-end q-mt-sm">
          <q-btn
            v-if="invoice.disable"
            label="Editar"
            color="amber"
            class="q-mr-sm"
            @click="invoice.disable = false"
          />
          <q-btn
            v-else
            label="Guardar"
            color="amber"
            class="q-mr-sm"
            @click="invoice.disable = true"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="
              (invoice.newInvoiceState = !invoice.newInvoiceState), (invoice.disable = false)
            "
          />
        </div>
      </div>

      <!-- Projects stages and owner -->

      <div class="row justify-center">
        <div v-if="!project.newProjectState" class="col q-mr-md">
          <div v-if="project.default">
            <SelectForm
              outlined
              class="row q-mr-md"
              :default_value="project.default"
              :disable="project.disable"
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
                  project.model = value;
                  project.name = projectOptions.find((x) => x.id === value).name;
                  getStagesData();
                }
              "
            />
          </div>

          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Proyecto"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="project.newProjectState = !project.newProjectState"
            />
          </div>
        </div>
        <div v-else class="col q-mr-lg">
          <div class="row">
            <q-input
              v-model="project.newProject"
              outlined
              label="Nombre proyeto"
              class="col"
              :disable="project.disable"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>

        <div v-if="!stage.newStageState && !project.newProjectState" class="col q-ml-md">
          <div v-if="stage.default">
            <SelectForm
              outlined
              class="row"
              :default_value="stage.default"
              :disable="project.disable"
              :options="stagesOptions"
              option_value="id"
              option_label="name"
              label="Etapas"
              not_found_label="No hay etapas disponibles"
              :rules="[
              /*val => !!val || 'Campo obligatorio'*/
              ]"
              lazy-rules
              @update-model="(value) => {
                stage.model = value;
                stage.name = stagesOptions.find((x) => x.id === value).name;
              }"
            />
          </div>

          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Etapa"
              icon="add"
              class="add-btn text-caption q-ml-md"
              @click="stage.newStageState = !stage.newStageState"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="stage.newStage"
              outlined
              label="Nombre etapa"
              class="col"
              :disable="project.disable"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
      </div>
      <div v-if="stage.newStageState || project.newProjectState" class="row justify-end">
        <q-btn
          v-if="project.disable"
          label="Editar"
          color="amber"
          class="q-mr-sm"
          @click="project.disable = false"
        />
        <q-btn
          v-else
          label="Guardar"
          color="amber"
          class="q-mr-sm"
          @click="project.disable = true"
        />
        <q-btn
          label="Ver lista"
          color="amber"
          @click="
            (stage.newStageState = false),
            (project.newProjectState = false),
            (project.disable = false)
          "
        />
      </div>
      <div v-if="project.newProjectState" class="row">
        <div v-if="!projectOwner.newProjectOwnerState" class="col">
          <div v-if="projectOwner.default">
            <SelectForm
              outlined
              class="row"
              :default_value="projectOwner.default"
              :disable="projectOwner.disable"
              :options="projectOwnersOptions"
              option_value="id"
              option_label="name"
              label="Dueño proyecto"
              not_found_label="No hay dueños disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  projectOwner.model = value;
                  projectOwner.name = projectOwnersOptions.find((x) => x.id === value).name;
                }
              "
            />
          </div>
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir dueño"
              color="amber"
              class="add-btn"
              @click="projectOwner.newProjectOwnerState = true"
            />
          </div>
        </div>
        <div v-else class="col">
          <q-input
            v-model="projectOwner.newProjectOwner"
            outlined
            class="row"
            label="Nombre dueño"
            :disable="projectOwner.disable"
            :rules="[(val) => !!val || 'Campo obligatorio']"
            lazy-rules
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              v-if="projectOwner.disable"
              label="Editar"
              color="amber"
              class="q-mr-sm"
              @click="projectOwner.disable = false"
            />
            <q-btn
              v-else
              label="Guardar"
              color="amber"
              class="q-mr-sm"
              @click="projectOwner.disable = true"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="
                (projectOwner.disable = false), (projectOwner.newProjectOwnerState = false)
              "
            />
          </div>
        </div>
      </div>
    </FormSection>
    <!-- Location -->
    <FormSection title="Datos ubicación">
      <div class="row justify-center">
        <div v-if="!building.newBuildingState" class="col q-mr-md">
          <div v-if="building.default">
            <SelectForm
              outlined
              class="row q-mr-md"
              :default_value="building.default"
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
                  building.model = value;
                  building.name = buildingOptions.find((x) => x.id === value).name;
                  getUnitsData();
                }
              "
            />
          </div>
          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir Edificio"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="building.newBuildingState = !building.newBuildingState"
            />
          </div>
        </div>
        <div v-else class="col">
          <div class="row">
            <q-input
              v-model="building.newBuilding"
              outlined
              label="Nombre edificio"
              class="col"
              :disable="disableLocation"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
            />
          </div>
        </div>
        <div v-if="!building.newBuildingState && !unit.newUnitState" class="col q-mr-md">
          <div v-if="unit.default">
            <SelectForm
              outlined
              class="row q-mr-md"
              :default_value="unit.default"
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
                  unit.model = value;
                  unit.name = value ? unitOptions.find((x) => x.id === value).name : null;
                  getRoomsData();
                }
              "
            />
          </div>

          <div class="row justify-end q-pt-md">
            <q-btn
              outlined
              label="Añadir unidad"
              icon="add"
              class="add-btn text-caption q-mr-md"
              @click="unit.newUnitState = !unit.newUnitState"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="unit.newUnit"
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
          v-if="!building.newBuildingState && !unit.newUnitState && !room.newRoomState"
          class="col"
        >
          <div v-if="room.default">
            <SelectForm
              outlined
              class="row"
              :default_value="room.default"
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
                  room.model = value;
                  room.name = value ? roomOptions.find((x) => x.id === value).name : null;
                }
              "
            />
          </div>

          <div class="row justify-end q-pt-md">
            <q-btn
              label="Añadir sala"
              icon="add"
              class="add-btn text-caption"
              @click="room.newRoomState = !room.newRoomState"
            />
          </div>
        </div>
        <div v-else class="col q-pl-md">
          <div class="row">
            <q-input
              v-model="room.newRoom"
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
        v-if="building.newBuildingState || unit.newUnitState || room.newRoomState"
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
            (building.newBuildingState = false),
            (unit.newUnitState = false),
            (room.newRoomState = false),
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
import { useRouter } from 'vue-router'
import { onMounted, reactive, ref } from 'vue'
import { useEquipmentFormStore } from 'src/stores'

import { getBrands, getBuildings, getInvoices, getInvoicesSupplier, getModelNumbers, getModels, getProjectOwners, getProjects, getRooms, getStages, getSuppliers, getUnits, postBrand, postBuilding, postEquipment, postEquipmentImage, postInvoice, postInvoiceImage, postModel, postModelNumber, postProject, postProjectOwner, postRoom, postStage, postUnit } from '/src/services'

import SelectForm from 'src/components/SelectForm.vue'
import UploadImages from 'src/components/UploadImages.vue'
import FormSection from 'src/components/Form/FormSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

const equipmentFormStore = useEquipmentFormStore()

const maintenanceOptions = [
  {
    id: 1,
    name: 'Mensual',
  },
  {
    id: 3,
    name: 'Trimestral',
  },
  {
    id: 6,
    name: 'Semestral',
  },
  {
    id: 12,
    name: 'Anual',
  },
]

const uploaderComponent = ref(null)

const brand = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newBrandState: false,
  newBrand: null,
})
const brandOptions = ref([])
const building = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newBuildingState: false,
  newBuilding: null,
})
const buildingOptions = ref([])
const createEquipmentForm = ref(null)
const disableLocation = ref(false)
const equipmentimages = ref([])
const invoiceimage = ref(null)
const name = ref(null)
const serial = ref(null)
const inventory = ref(0)
const invoice = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newInvoiceState: false,
  newInvoiceNumber: null,
  newInvoiceDate: null,

})
const invoicesOptions = ref([])
const loading = ref(false)
const model = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newModelState: false,
  newModel: null,
})
const modelOptions = ref([])
const modelNumber = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newModelNumberState: false,
  newModelNumber: null,
})
const modelNumberOptions = ref([])
const maintenance = reactive({
  model: null,
  name: null,
  default: null,
  apply: false,
})
const observation = ref(null)
const project = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newProjectState: false,
  newProject: null,
})
const projectOwner = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newProjectOwnerState: false,
  newProjectOwner: null,
})
const projectOptions = ref([])
const projectOwnersOptions = ref([])
const reception_date = ref(null)
const stage = reactive({
  model: null,
  name: null,
  default: null,
  newStageState: false,
  newStage: null,
})
const stagesOptions = ref([])
const room = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newRoomState: false,
  newRoom: null,
})
const roomOptions = ref([])
const supplier = ref(null)
const suppliersOptions = ref([])
const unit = reactive({
  model: null,
  name: null,
  default: null,
  disable: false,
  newUnitState: false,
  newUnit: null,
})
const unitOptions = ref([])
const router = useRouter()

function handleAddImages(files) {
  equipmentimages.value.push(files[0])
}

function handleRemoveImages(files) {
  equipmentimages.value = equipmentimages.value.filter((value) => {
    return value !== files[0]
  })
}

async function loadEquipmentFromStore() {
  const storeEquipment = equipmentFormStore.equipment
  if (Object.keys(storeEquipment).length === 0) {
    brand.default = { id: null, name: null }
    building.default = { id: null, name: null }
    maintenance.default = { id: null, name: null }
    model.default = { id: null, name: null }
    modelNumber.default = { id: null, name: null }
    unit.default = { id: null, name: null }
    room.default = { id: null, name: null }
    invoice.default = { id: null, name: null }
    project.default = { id: null, name: null }
    projectOwner.default = { id: null, name: null }
    stage.default = { id: null, name: null }
    return
  }
  building.model = storeEquipment.value.building.model
  building.default = storeEquipment.value.building.default
  building.disable = storeEquipment.value.building.disable
  building.name = storeEquipment.value.building.name
  building.newBuildingState = storeEquipment.value.building.newBuildingState
  building.newBuilding = storeEquipment.value.building.newBuilding
  buildingOptions.value = storeEquipment.value.buildingOptions
  name.value = storeEquipment.value.name
  serial.value = storeEquipment.value.serial
  inventory.value = storeEquipment.value.inventory
  invoiceimage.value = storeEquipment.value.invoiceimage
  model.model = storeEquipment.value.model.model
  model.name = storeEquipment.value.model.name
  model.default = storeEquipment.value.model.default
  model.disable = storeEquipment.value.model.disable
  model.newModelState = storeEquipment.value.model.newModelState
  model.newModel = storeEquipment.value.model.newModel
  modelOptions.value = storeEquipment.value.modelOptions
  modelNumber.model = storeEquipment.value.modelNumber.model
  modelNumber.name = storeEquipment.value.modelNumber.name
  modelNumber.default = storeEquipment.value.modelNumber.default
  modelNumber.disable = storeEquipment.value.modelNumber.disable
  modelNumber.newModelNumberState = storeEquipment.value.modelNumber.newModelNumberState
  modelNumber.newModelNumber = storeEquipment.value.modelNumber.newModelNumber
  modelNumberOptions.value = storeEquipment.value.modelNumberOptions
  maintenance.apply = storeEquipment.value.maintenance.apply
  maintenance.model = storeEquipment.value.maintenance.model
  maintenance.name = storeEquipment.value.maintenance.name
  maintenance.default = storeEquipment.value.maintenance.default
  observation.value = storeEquipment.value.observation
  reception_date.value = storeEquipment.value.reception_date
  brand.model = storeEquipment.value.brand.model
  brand.name = storeEquipment.value.brand.name
  brand.default = storeEquipment.value.brand.default
  brand.disable = storeEquipment.value.brand.disable
  brand.newBrandState = storeEquipment.value.brand.newBrandState
  brand.newBrand = storeEquipment.value.brand.newBrand
  brandOptions.value = storeEquipment.value.brandOptions
  unit.model = storeEquipment.value.unit.model
  unit.name = storeEquipment.value.unit.name
  unit.default = storeEquipment.value.unit.default
  unit.disable = storeEquipment.value.unit.disable
  unit.newUnitState = storeEquipment.value.unit.newUnitState
  unit.newUnit = storeEquipment.value.unit.newUnit
  unitOptions.value = storeEquipment.value.unitOptions
  room.model = storeEquipment.value.room.model
  room.name = storeEquipment.value.room.name
  room.default = storeEquipment.value.room.default
  room.disable = storeEquipment.value.room.disable
  room.newRoomState = storeEquipment.value.room.newRoomState
  room.newRoom = storeEquipment.value.room.newRoom
  roomOptions.value = storeEquipment.value.roomOptions
  projectOwner.model = storeEquipment.value.projectOwner.model
  projectOwner.name = storeEquipment.value.projectOwner.name
  projectOwner.default = storeEquipment.value.projectOwner.default
  projectOwner.disable = storeEquipment.value.projectOwner.disable
  projectOwner.newProjectOwnerState = storeEquipment.value.projectOwner.newProjectOwnerState
  projectOwner.newProjectOwner = storeEquipment.value.projectOwner.newProjectOwner
  projectOwnersOptions.value = storeEquipment.value.projectOwnersOptions
  project.model = storeEquipment.value.project.model
  project.name = storeEquipment.value.project.name
  project.default = storeEquipment.value.project.default
  project.disable = storeEquipment.value.project.disable
  project.newProjectState = storeEquipment.value.project.newProjectState
  project.newProject = storeEquipment.value.project.newProject
  projectOptions.value = storeEquipment.value.projectOptions
  stage.model = storeEquipment.value.stage.model
  stage.name = storeEquipment.value.stage.name
  stage.default = storeEquipment.value.stage.default
  stage.newStageState = storeEquipment.value.stage.newStageState
  stage.newStage = storeEquipment.value.stage.newStage
  stagesOptions.value = storeEquipment.value.stagesOptions
  supplier.value = storeEquipment.value.supplier
  invoice.model = storeEquipment.value.invoice.model
  invoice.name = storeEquipment.value.invoice.name
  invoice.default = storeEquipment.value.invoice.default
  invoice.disable = storeEquipment.value.invoice.disable
  invoice.newInvoiceState = storeEquipment.value.invoice.newInvoiceState
  invoice.newInvoiceDate = storeEquipment.value.invoice.newInvoiceDate
  invoice.newInvoiceNumber = storeEquipment.value.invoice.newInvoiceNumber
  invoicesOptions.value = storeEquipment.value.invoicesOptions
  uploaderComponent.value.addFiles(storeEquipment.value.equipmentimages)
  equipmentFormStore.clearEquipmentForm()
}

function newSupplier() {
  brand.default = { id: brand.model, name: brand.name }
  building.default = { id: building.model, name: building.name }
  maintenance.default = { id: maintenance.model, name: maintenance.name }
  model.default = { id: model.model, name: model.name }
  modelNumber.default = { id: modelNumber.model, name: modelNumber.name }
  unit.default = { id: unit.model, name: unit.name }
  room.default = { id: room.model, name: room.name }
  invoice.default = { id: invoice.model, name: invoice.name }
  project.default = { id: project.model, name: project.name }
  projectOwner.default = { id: projectOwner.model, name: projectOwner.name }
  stage.default = { id: stage.model, name: stage.name }
  equipmentFormStore.setRedirectTo()
  equipmentFormStore.setEquipment({
    name: name.value,
    serial: serial.value,
    inventory: inventory.value,
    invoiceimage: invoiceimage.value,
    model,
    modelOptions: modelOptions.value,
    modelNumber,
    modelNumberOptions: modelNumberOptions.value,
    maintenance,
    observation: observation.value,
    reception_date: reception_date.value,
    brand,
    brandOptions: brandOptions.value,
    building,
    buildingOptions: buildingOptions.value,
    unit,
    unitOptions: unitOptions.value,
    room,
    roomOptions: roomOptions.value,
    project,
    projectOptions: projectOptions.value,
    projectOwner,
    projectOwnersOptions: projectOwnersOptions.value,
    stage,
    stagesOptions: stagesOptions.value,
    supplier: supplier.value,
    invoice,
    invoicesOptions: invoicesOptions.value,
    equipmentimages: equipmentimages.value,
    uploaderComponent: uploaderComponent.value,
  })
  router.push('/suppliers/new_supplier')
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
  const models = await getModels(brand.model)
  modelOptions.value = models.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getModelNumbersData() {
  const modelnumbers = await getModelNumbers(model.model)
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
  const rooms = await getRooms(unit.model)
  room.model = null
  room.default = { id: null, name: null }
  roomOptions.value = rooms.map((x) => {
    return { id: x.id, name: x.name }
  })
}

async function getStagesData() {
  const stages = await getStages(project.model)
  stage.model = null
  stage.default = { id: null, name: null }
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
  const units = await getUnits(building.model)
  unit.model = null
  unit.default = { id: null, name: null }
  room.model = null
  room.default = { id: null, name: null }
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
  if (!brand.newBrandState)
    return brand.model

  const brandData = {
    name: brand.newBrand,
  }

  return await postBrand(brandData)
}

async function createNewBuilding() {
  if (!building.newBuildingState)
    return building.model

  const buildingData = {
    name: building.newBuilding,
  }

  return await postBuilding(buildingData)
}

async function createNewInvoice(supplier_id) {
  if (!invoice.newInvoiceState)
    return invoice.model

  const invoiceData = {
    number: invoice.newInvoiceNumber,
    date: invoice.newInvoiceDate,
    supplier_id,
  }

  return await postInvoice(invoiceData)
}

async function createNewModel(brand_id) {
  if (!brand.newBrandState && !model.newModelState)
    return model.model

  const newmodelData = {
    name: model.newModel,
    brand_id,
  }

  return await postModel(newmodelData)
}

async function createNewModelnumber(model_id) {
  if (!brand.newBrandState && !model.newModelState && !modelNumber.newModelNumber)
    return modelNumber.model

  const newModelNumberData = {
    number: modelNumber.newModelNumber,
    model_id,
  }

  return await postModelNumber(newModelNumberData)
}

async function createNewProject(project_owner_id) {
  if (!project.newProjectState)
    return project.model

  const projectname = project.newProject

  if (projectname.trim().length === 0)
    return -1

  if (project_owner_id === -1)
    project_owner_id = null

  const projectData = {
    name: projectname,
    owner_id: project_owner_id,
  }

  return await postProject(projectData)
}

async function createNewProjectOwner() {
  if (!projectOwner.newProjectOwnerState)
    return projectOwner.model

  const projectownername = projectOwner.newProjectOwner

  if (projectownername.trim().length === 0)
    return -1

  const projectownerdata = {
    name: projectownername,
  }

  return await postProjectOwner(projectownerdata)
}

async function createNewUnit(building_id) {
  if (!building.newBuildingState && !unit.newUnitState)
    return unit.model

  const unitData = {
    name: unit.newUnit,
    building_id,
  }

  return await postUnit(unitData)
}

async function createNewRoom(unit_id) {
  if (!building.newBuildingState && !unit.newUnitState && !room.newRoomState)
    return room.model

  const roomData = {
    name: room.newRoom,
    unit_id,
  }

  return await postRoom(roomData)
}

async function createNewStage(project_id) {
  if (!stage.newStageState && !project.newProjectState)
    return stage.model

  const stagename = stage.newStage

  if (stagename.trim().length === 0)
    return -1

  const stageData = {
    name: stage.newStage,
    project_id,
  }

  return await postStage(stageData)
}

async function createNewEquipment(equipmentData) {
  return await postEquipment(equipmentData)
}

async function uploadInvoiceImage(equipment_id) {
  if (!invoice.newInvoiceState || invoiceimage.value == null)
    return

  const formData = new FormData()
  formData.append('file', invoiceimage.value)
  await postInvoiceImage(equipment_id, formData)
}

async function uploadEquipmentImage(equipment_id) {
  if (equipmentimages.value == null)
    return

  equipmentimages.value.forEach(async (image) => {
    const formData = new FormData()
    formData.append('file', image)
    await postEquipmentImage(equipment_id, formData)
  })
}

async function onSubmit() {
  createEquipmentForm.value.resetValidation()
  const equipmentdata = {
    name: name.value,
    serial_number: serial.value,
    umag_inventory_code: inventory.value,
    reception_date: reception_date.value,
    observation: observation.value,
    model_number_id: modelNumber.model,
    supplier_id: supplier.value,
    invoice_id: invoice.model,
    room_id: room.model,
    stage_id: stage.model,
    last_preventive_mainteinance: reception_date.value,
  }
  loading.value = true
  if (maintenance.apply)
    equipmentdata.maintenance_period = maintenance.model

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

  const invoice_id = await createNewInvoice(equipmentdata.supplier_id)
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
  loadEquipmentFromStore()
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
