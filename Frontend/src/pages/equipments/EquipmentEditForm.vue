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
            <InputSelect
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
            <InputSelect
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
            <InputSelect
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

      <div class="row">
        <q-checkbox
          v-model="isRelevant"
          val="lg"
          label="¿El equipo es relevante?"
        />
      </div>

      <!-- Mantenimiento -->
      <q-checkbox
        v-model="maintenance.apply"
        val="lg"
        label="Aplica para mantención"
      />
      <div v-if="maintenance.default !== null">
        <InputSelect
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
      <div v-if="supplier.default">
        <InputSelect
          outlined
          :options="suppliersOptions"
          :default_value="supplier.default"
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
              (supplier.model = value), getInvoicesSupplierData(value);
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
        <div v-if="invoice.default">
          <InputSelect
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
        </div>

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
            <InputSelect
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
            <InputSelect
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
            <InputSelect
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
            <InputSelect
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
            <InputSelect
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
            <InputSelect
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
      <q-btn label="Guardar" type="submit" color="positive" />
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
import { useRoute, useRouter } from 'vue-router'
import { onMounted, reactive, ref } from 'vue'

import { deleteImage, getBrands, getBuildings, getEquipment, getEquipmentImages, getImage, getInvoices, getInvoicesSupplier, getModelNumbers, getModels, getProjectOwners, getProjects, getRooms, getStages, getSuppliers, getUnits, postBrand, postBuilding, postEquipmentImage, postInvoice, postInvoiceImage, postModel, postModelNumber, postProject, postProjectOwner, postRoom, postStage, postUnit, updateEquipment } from '/src/services'

import InputSelect from 'src/components/form/inputs/InputSelect.vue'
import UploadImages from 'src/components/UploadImages.vue'
import FormSection from 'src/components/form/FormSection.vue'
import PageTitle from 'src/components/commons/PageTitle.vue'

const route = useRoute()
const id = ref(route.params.id)

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
const supplier = reactive({
  model: null,
  name: null,
  default: null,
})
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
const originalImages = ref([])
const isRelevant = ref(false)

const router = useRouter()

async function getEquipmentData() {
  const defaultEquipment = await getEquipment(id.value)
  name.value = defaultEquipment.name
  serial.value = defaultEquipment.serial_number
  inventory.value = defaultEquipment.umag_inventory_code
  maintenance.apply = !!defaultEquipment.maintenance_period
  observation.value = defaultEquipment.observation
  reception_date.value = defaultEquipment.reception_date
  isRelevant.value = defaultEquipment.relevant
  brand.default = { id: defaultEquipment.brand_id, name: defaultEquipment.brand_name }
  brand.model = defaultEquipment.brand_id
  brand.name = defaultEquipment.brand_name
  const models = await getModels(brand.model)
  modelOptions.value = models.map((x) => {
    return { id: x.id, name: x.name }
  })
  model.default = { id: defaultEquipment.model_id, name: defaultEquipment.model_name }
  model.model = defaultEquipment.model_id
  model.name = defaultEquipment.model_name
  const modelNumbers = await getModelNumbers(model.model)
  modelNumberOptions.value = modelNumbers.map((x) => {
    return { id: x.id, name: x.number }
  })
  modelNumber.default = { id: defaultEquipment.model_number_id, name: defaultEquipment.model_number }
  modelNumber.model = defaultEquipment.model_number_id
  modelNumber.name = defaultEquipment.model_number
  building.default = { id: defaultEquipment.building_id, name: defaultEquipment.building_name }
  building.model = defaultEquipment.building_id
  building.name = defaultEquipment.building_name
  const units = await getUnits(building.model)
  unitOptions.value = units.map((x) => {
    return { id: x.id, name: x.name }
  })
  unit.default = { id: defaultEquipment.unit_id, name: defaultEquipment.unit_name }
  unit.model = defaultEquipment.unit_id
  unit.name = defaultEquipment.unit_name
  const rooms = await getRooms(unit.model)
  roomOptions.value = rooms.map((x) => {
    return { id: x.id, name: x.name }
  })
  room.default = { id: defaultEquipment.room_id, name: defaultEquipment.room_name }
  room.model = defaultEquipment.room_id
  room.name = defaultEquipment.room_name
  maintenance.default = defaultEquipment.maintenance_period ? { id: defaultEquipment.maintenance_period, name: maintenanceOptions.find(x => x.id === defaultEquipment.maintenance_period).name } : { id: null, name: null }
  maintenance.model = defaultEquipment.maintenance_period
  maintenance.name = maintenanceOptions.find(x => x.id === defaultEquipment.maintenance_period).name
  supplier.default = { id: defaultEquipment.supplier_id, name: defaultEquipment.supplier_name }
  supplier.model = defaultEquipment.supplier_id
  supplier.name = defaultEquipment.supplier_name
  invoice.default = { id: defaultEquipment.invoice_id, name: defaultEquipment.invoice_number }
  invoice.model = defaultEquipment.invoice_id
  invoice.name = defaultEquipment.invoice_number
  project.default = { id: defaultEquipment.project_id, name: defaultEquipment.project_name }
  project.model = defaultEquipment.project_id
  project.name = defaultEquipment.project_name
  const stages = await getStages(project.model)
  stagesOptions.value = stages.map((x) => {
    return { id: x.id, name: x.name }
  })
  stage.default = { id: defaultEquipment.stage_id, name: defaultEquipment.stage_name }
  stage.model = defaultEquipment.stage_id
  stage.name = defaultEquipment.stage_name
  projectOwner.default = { id: defaultEquipment.project_owner_id, name: defaultEquipment.project_owner_name }
  projectOwner.model = defaultEquipment.project_owner_id
  projectOwner.name = defaultEquipment.project_owner_name
  getImages()
}

async function getImages() {
  const equipmentImages = await getEquipmentImages(id.value)
  equipmentImages.map(async (image) => {
    const blob = await getImage(image.path)
    const imageFile = new File([blob], image.name, { type: blob.type, __img: 'img', __key: image.name, __progress: 0, __progressLabel: '0.00%', __status: 'idle', __uploaded: 0 })
    uploaderComponent.value.addFiles([imageFile])
    originalImages.value.push(imageFile)
  })
}

function handleAddImages(files) {
  equipmentimages.value.push(files[0])
}

function handleRemoveImages(files) {
  equipmentimages.value = equipmentimages.value.filter((value) => {
    return value !== files[0]
  })
}

function newSupplier() {
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

async function uploadInvoiceImage(equipment_id) {
  if (!invoice.newInvoiceState || invoiceimage.value == null)
    return

  const formData = new FormData()
  formData.append('file', invoiceimage.value)
  await postInvoiceImage(equipment_id, formData)
}

async function uploadEquipmentImage(equipment_id) {
  const deleteImages = originalImages.value.filter((image) => {
    return !equipmentimages.value.includes(image)
  })

  const newImages = equipmentimages.value.filter((image) => {
    return !originalImages.value.includes(image)
  })

  // Delete the old images
  if (deleteImages.length > 0) {
    deleteImages.forEach(async (image) => {
      const formData = new FormData()
      formData.append('file', image)
      await deleteImage('equipments', id.value, formData)
    })
  }
  if (newImages.length === 0)
    return

  newImages.forEach(async (image) => {
    const formData = new FormData()
    formData.append('file', image)
    await postEquipmentImage(equipment_id, formData)
  })
}

async function onSubmit() {
  createEquipmentForm.value.resetValidation()
  const equipmentdata = {
    id: id.value,
    name: name.value,
    serial_number: serial.value,
    umag_inventory_code: inventory.value,
    reception_date: reception_date.value,
    relevant: isRelevant.value,
    observation: observation.value,
    model_number_id: modelNumber.model,
    supplier_id: supplier.model,
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
  const equipment_id = await updateEquipment(id.value, equipmentdata)
  await uploadEquipmentImage(equipment_id)
  await uploadInvoiceImage(equipment_id)
  loading.value = false
  // onReset()

  redirectToEquipment(equipment_id.toString())
}

function redirectToEquipment(equipment_id) {
  router.push({ path: `/equipments/${equipment_id}` })
}

onMounted(() => {
  getBrandsData()
  getInvoicesData()
  getProjectsData()
  getProjectOwnersData()
  getSuppliersData()
  getBuildingsData()
  getEquipmentData()
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
  appearance: textfield;
}
</style>
