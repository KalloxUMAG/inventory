<template>
  <q-page class="q-ma-sm">
    <div class="row justify-center">
      <q-form
        @submit.prevent="onSubmit"
        @reset="onReset"
        class="q-gutter-md col-xs-12 col-sm-12 col-md-6 q-pa-md relative-position bg-grey-4"
        ref="createEquipmentForm"
      >
        <!--Datos Producto-->

        <q-input
          filled
          v-model="name"
          maxlength="49"
          label="Nombre del equipo*"
          lazy-rules
          :rules="[
            (val) => (val && val.length > 0) || 'Este campo es obligatorio',
            (val) =>
              (val && val.length < 50) ||
              'El nombre debe contener menos de 50 caracteres',
          ]"
        />
        <q-input
          filled
          v-model="serial"
          maxlength="30"
          label="Código serial*"
          lazy-rules
          :rules="[
            (val) => (val && val.length > 0) || 'Este campo es obligatorio',
            (val) => (val && val.length < 256) || 'Máximo 255 caracteres',
          ]"
        />
        <q-input
          filled
          v-model="inventory"
          maxlength="11"
          type="number"
          label="Inventario UMAG*"
          lazy-rules
          :rules="[
            (val) =>
              (val.length < 26 && val > 0) ||
              'El valor debe ser mayor que 0 y tener un maximo de 25 dígitos',
          ]"
        />

        <!--Brand Model Number-->

        <div class="row justify-center">
          <div v-if="!newbrandstate" class="col q-mr-md">
            <SelectForm
              class="row q-mr-md"
              :disable="disableBrand"
              :options="brandOptions"
              option_value="id"
              option_label="name"
              label="Marca"
              not_found_label="No hay marcas disponibles"
              @updateModel="
                (value) => {
                  brand = value;
                  getModels();
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir marca"
                icon="add"
                class="bg-green-3 text-caption q-mr-md"
                @click="newbrandstate = !newbrandstate"
              />
            </div>
          </div>
          <div v-else class="col">
            <div class="row">
              <q-input v-model="newbrand" label="Nombre marca" class="col" :disable="disableBrand"/>
            </div>
          </div>
          <div v-if="!newbrandstate && !newmodelstate" class="col q-mr-md">
            <SelectForm
              class="row q-mr-md"
              :disable="disableBrand"
              :options="modelOptions"
              option_value="id"
              option_label="name"
              label="Modelo"
              not_found_label="No hay modelos disponibles"
              @updateModel="
                (value) => {
                  model = value;
                  getModelNumbers();
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir modelo"
                icon="add"
                class="bg-green-3 text-caption q-mr-md"
                @click="newmodelstate = !newmodelstate"
              />
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input v-model="newmodel" label="Nombre modelo" class="col" :disable="disableBrand"/>
            </div>
          </div>
          <div
            v-if="!newbrandstate && !newmodelstate && !newmodelnumberstate"
            class="col"
          >
            <SelectForm
              class="row"
              :disable="disableBrand"
              :options="modelNumberOptions"
              option_value="id"
              option_label="name"
              label="Número modelo"
              not_found_label="No hay número de modelo disponibles"
              @updateModel="
                (value) => {
                  modelNumber = value;
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir número modelo"
                icon="add"
                class="bg-green-3 text-caption"
                @click="newmodelnumberstate = !newmodelnumberstate"
              />
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input
                v-model="newmodelnumber"
                label="Número modelo"
                class="col"
                :disable="disableBrand"
              />
            </div>
          </div>
        </div>
        <div v-if="newmodelstate || newmodelnumberstate || newbrandstate" class="row justify-end q-pt-md">

          <q-btn v-if="disableBrand"
            label="Editar"
            color="amber"
            @click="disableBrand = false"
            class="q-mr-sm"
          />
          <q-btn v-else
            label="Guardar"
            color="amber"
            @click="disableBrand = true"
            class="q-mr-sm"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="newmodelnumberstate = false, newmodelstate = false, newbrandstate = false, disableBrand = false"
          />
        </div>

        <!--Mantenimiento-->
        <q-checkbox
          v-model="maintenanceApply"
          val="lg"
          label="Aplica para mantención"
        />
        <SelectForm
          v-if="maintenanceApply"
          :options="maintenanceOptions"
          option_value="value"
          option_label="name"
          label="Periodo de mantención"
          not_found_label="No hay periodos disponibles"
          @updateModel="(value) => (maintenance = value)"
        />
        <!--Observacion-->
        <q-input
          filled
          v-model="observation"
          type="textarea"
          label="Observación"
          lazy-rules
        />

        <!--Imagenes equipamiento equipmentImages-->
        <div class="row">
          <div class="col">
            <q-file
              v-model="equipmentimages"
              label="Selecciona imagenes para el equipo"
              filled
              counter
              max-files="5"
              multiple
              accept=".jpg, image/*"
              clearable
            >
              <template v-slot:prepend>
                <q-icon name="cloud_upload" />
              </template>
            </q-file>
          </div>
        </div>

        <!--Datos de compra-->
        <!--Datos de proveedor-->
        <div v-if="!newsupplierstate">
          <SelectForm
            :options="suppliersOptions"
            option_value="id"
            option_label="name"
            label="Proveedor"
            not_found_label="No hay proveedores disponibles"
            @updateModel="(value) => {supplier = value, getInvoicesSupplier(value)}"
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir proveedor"
              icon="add"
              class="bg-green-3 text-caption"
              @click="newsupplierstate = !newsupplierstate"
            />
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input
              v-model="newsuppliername"
              label="Nombre proveedor"
              class="col"
              :disable="disableSupplier"
            />
            <q-input v-model="newsupplierrut" label="Rut" class="col q-ml-md" :disable="disableSupplier"/>
            <q-input
              v-model="newsupplieraddress"
              label="Dirección"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row q-mt-sm">
            <q-input
              v-model="workername1"
              label="Nombre trabajador"
              class="col"
              :disable="disableSupplier"
            />
            <SelectForm
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              @updateModel="(value) => (workerrol1 = value)"
              class="col q-ml-md"
            />
            <q-input
              v-model="workermail1"
              label="Correo trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
            <q-input
              v-model="workerphone1"
              label="Telefono trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row q-mt-sm">
            <q-input
              v-model="workername2"
              label="Nombre trabajador"
              class="col"
              :disable="disableSupplier"
            />
            <SelectForm
              :disable="disableSupplier"
              :options="rolOptions"
              option_value="value"
              option_label="name"
              label="Roles"
              not_found_label="No hay roles disponibles"
              @updateModel="(value) => (workerrol2 = value)"
              class="col q-ml-md"
            />
            <q-input
              v-model="workermail2"
              label="Correo trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
            <q-input
              v-model="workerphone2"
              label="Telefono trabajador"
              class="col q-ml-md"
              :disable="disableSupplier"
            />
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn v-if="disableSupplier"
              label="Editar"
              color="amber"
              @click="disableSupplier = false"
              class="q-mr-sm"
            />
            <q-btn v-else
              label="Guardar"
              color="amber"
              @click="disableSupplier = true"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="newsupplierstate = !newsupplierstate, disableSupplier = false"
            />
          </div>
        </div>

        <q-input
          filled
          v-model="reception_date"
          type="date"
          label="Fecha de recepción*"
          stack-label
          lazy-rules
          :rules="[
            (val) => (val && val != null) || 'Este campo es obligatorio',
          ]"
        />

        <!--Invoices-->
        <div v-if="!newinvoicestate">
          <SelectForm
            :options="invoicesOptions"
            option_value="id"
            option_label="name"
            label="Facturas"
            not_found_label="No hay facturas disponibles"
            @updateModel="(value) => (invoice = value)"
          />
          <div class="row justify-end q-mt-md">
            <q-btn
              label="Añadir factura"
              icon="add"
              class="bg-green-3 text-caption"
              @click="newinvoicestate = !newinvoicestate"
            />
          </div>
        </div>

        <div v-else>
          <div class="row">
            <q-input
              v-model="newinvoicenumber"
              label="Numero"
              type="number"
              class="col"
              :disable="disableInvoice"
            />
            <q-input
              v-model="newinvoicedate"
              label="Fecha"
              type="date"
              stack-label
              class="col q-ml-md"
              :disable="disableInvoice"
            />
          </div>
          <div class="row q-mt-sm">
            <q-file
              class="col"
              v-model="invoiceimage"
              filled
              label="Foto de factura"
              accept=".jpg, image/*"
              :disable="disableInvoice"
              clearable
            >
              <template v-slot:prepend>
                <q-icon name="cloud_upload" />
              </template>
            </q-file>
          </div>
          <div class="row justify-end q-mt-sm">
            <q-btn v-if="disableInvoice"
              label="Editar"
              color="amber"
              @click="disableInvoice = false"
              class="q-mr-sm"
            />
            <q-btn v-else
              label="Guardar"
              color="amber"
              @click="disableInvoice = true"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver lista"
              color="amber"
              @click="newinvoicestate = !newinvoicestate, disableInvoice = false"
            />
          </div>
        </div>

        <!--Projects stages and owner-->

        <div class="row justify-center">
          <div v-if="!newprojectstate" class="col q-mr-md">
            <SelectForm
              class="row q-mr-md"
              :disable="disableProject"
              :options="projectOptions"
              option_value="id"
              option_label="name"
              label="Proyectos"
              not_found_label="No hay proyectos disponibles"
              @updateModel="
                (value) => {
                  project = value;
                  getStages();
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir Proyecto"
                icon="add"
                class="bg-green-3 text-caption q-mr-md"
                @click="newprojectstate = !newprojectstate"
              />
            </div>
          </div>
          <div v-else class="col q-mr-lg">
            <div class="row">
              <q-input
                v-model="newprojectname"
                label="Nombre proyeto"
                class="col"
                :disable="disableProject"
              />
            </div>
          </div>

          <div v-if="!newstagestate && !newprojectstate" class="col q-ml-md">
            <SelectForm
              class="row"
              :disable="disableProject"
              :options="stagesOptions"
              option_value="id"
              option_label="name"
              label="Etapas"
              not_found_label="No hay etapas disponibles"
              @updateModel="(value) => (stage = value)"
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir Etapa"
                icon="add"
                class="bg-green-3 text-caption q-ml-md"
                @click="newstagestate = !newstagestate"
              />
            </div>
          </div>
          <div v-else class="col">
            <div class="row">
              <q-input
                v-model="newstagename"
                label="Nombre etapa"
                class="col"
                :disable="disableProject"
              />
            </div>
          </div>
        </div>
        <div v-if="newstagestate || newprojectstate" class="row justify-end">
          <q-btn v-if="disableProject"
            label="Editar"
            color="amber"
            @click="disableProject = false"
            class="q-mr-sm"
          />
          <q-btn v-else
            label="Guardar"
            color="amber"
            @click="disableProject = true"
            class="q-mr-sm"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="newstagestate = false, newprojectstate = false, disableProject = false"
            />
        </div>
        <div v-if="newprojectstate" class="row">
          <div v-if="!newProjectOwnerState" class="col">
            <SelectForm
              class="row"
              :disable="disableProjectOwner"
              :options="projectOwnersOptions"
              option_value="id"
              option_label="name"
              label="Patrocinador"
              not_found_label="No hay patrocinadores disponibles"
              @updateModel="
                (value) => {
                  projectowner = value;
                }
              "
            />
            <div class="row justify-end q-mt-md">
              <q-btn
                label="Añadir patrocinador"
                color="amber"
                @click="newProjectOwnerState = true"
              />
            </div>
          </div>
          <div v-else class="col">
            <q-input
              class="row"
              v-model="newprojectownername"
              label="Nombre patrocinador"
              :disable="disableProjectOwner"
            />
            <div class="row justify-end q-mt-md">
              <q-btn v-if="disableProjectOwner"
                label="Editar"
                color="amber"
                @click="disableProjectOwner = false"
                class="q-mr-sm"
              />
              <q-btn v-else
                label="Guardar"
                color="amber"
                @click="disableProjectOwner = true"
                class="q-mr-sm"
              />
              <q-btn
                label="Ver lista"
                color="amber"
                @click="disableProjectOwner = false, newProjectOwnerState = false"
              />
            </div>
          </div>
        </div>

        <!--Location-->
        <div class="row justify-center">
          <div v-if="!newbuildingstate" class="col q-mr-md">
            <SelectForm
              class="row q-mr-md"
              :disable="disableLocation"
              :options="buildingOptions"
              option_value="id"
              option_label="name"
              label="Edificio"
              not_found_label="No hay edificios disponibles"
              @updateModel="
                (value) => {
                  building = value;
                  getUnits();
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir Edificio"
                icon="add"
                class="bg-green-3 text-caption q-mr-md"
                @click="newbuildingstate = !newbuildingstate"
              />
            </div>
          </div>
          <div v-else class="col">
            <div class="row">
              <q-input
                v-model="newbuildingname"
                label="Nombre edificio"
                class="col"
                :disable="disableLocation"
              />
            </div>
          </div>
          <div v-if="!newbuildingstate && !newunitstate" class="col q-mr-md">
            <SelectForm
              class="row q-mr-md"
              :disable="disableLocation"
              :options="unitOptions"
              option_value="id"
              option_label="name"
              label="Unidad"
              not_found_label="No hay una unidad disponible"
              @updateModel="
                (value) => {
                  unit = value;
                  getRooms();
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir unidad"
                icon="add"
                class="bg-green-3 text-caption q-mr-md"
                @click="newunitstate = !newunitstate"
              />
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input
                v-model="newunitname"
                label="Nombre unidad"
                class="col"
                :disable="disableLocation"
              />
            </div>
          </div>
          <div
            v-if="!newbuildingstate && !newunitstate && !newroomstate"
            class="col"
          >
            <SelectForm
              class="row"
              :disable="disableLocation"
              :options="roomOptions"
              option_value="id"
              option_label="name"
              label="Sala"
              not_found_label="No hay salas disponibles"
              @updateModel="
                (value) => {
                  room = value;
                }
              "
            />
            <div class="row justify-end q-pt-md">
              <q-btn
                label="Añadir sala"
                icon="add"
                class="bg-green-3 text-caption"
                @click="newroomstate = !newroomstate"
              />
            </div>
          </div>
          <div v-else class="col q-pl-md">
            <div class="row">
              <q-input v-model="newroomname" label="Nombre sala" class="col" :disable="disableLocation"/>
            </div>
          </div>
        </div>
        <div v-if="newbuildingstate || newunitstate || newroomstate" class="row justify-end">
          <q-btn v-if="disableLocation"
            label="Editar"
            color="amber"
            @click="disableLocation = false"
            class="q-mr-sm"
          />
          <q-btn v-else
            label="Guardar"
            color="amber"
            @click="disableLocation = true"
            class="q-mr-sm"
          />
          <q-btn
            label="Ver lista"
            color="amber"
            @click="newbuildingstate = false, newunitstate = false, newroomstate = false,  disableLocation = false"
          />
        </div>

        <!--Form button-->
        <div class="row justify-end">
          <q-btn label="Crear" type="submit" color="primary" />
          <q-btn
            label="Limpiar campos"
            type="reset"
            color="primary"
            flat
            class="q-ml-sm"
          />
        </div>
        <q-inner-loading
          :showing="loading"
          label="Creando equipamiento"
          label-class="text-deep-orange"
          label-style="font-size: 1.6em"
        />
      </q-form>
    </div>
  </q-page>
</template>

<script setup>
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";
import SelectForm from "src/components/SelectForm.vue";

const maintenanceOptions = [
  {
    value: 1,
    name: "Mensual",
  },
  {
    value: 3,
    name: "Trimestral",
  },
  {
    value: 6,
    name: "Semestral",
  },
  {
    value: 12,
    name: "Anual",
  },
];

const rolOptions = [
  {
    value: "Vendedor",
    name: "Vendedor",
  },
  {
    value: "Tecnico",
    name: "Tecnico",
  },
];

const brand = ref(null);
const brandOptions = ref([]);
const building = ref(null);
const buildingOptions = ref([]);
const createEquipmentForm = ref(null);
const disableBrand = ref(false)
const disableInvoice = ref(false)
const disableLocation = ref(false)
const disableProject = ref(false)
const disableProjectOwner = ref(false)
const disableSupplier = ref(false)
const equipmentimages = ref(null);
const invoiceimage = ref(null);
const name = ref(null);
const serial = ref(null);
const inventory = ref(null);
const invoice = ref(null);
const invoicesOptions = ref([]);
const loading = ref(false);
const model = ref(null);
const modelOptions = ref([]);
const modelNumber = ref(null);
const modelNumberOptions = ref([]);
const maintenance = ref(null);
const observation = ref(null);
const newbrandstate = ref(false);
const newbuildingname = ref(null);
const newbuildingstate = ref(false);
const newinvoicestate = ref(false);
const newmodelstate = ref(null);
const newmodelnumberstate = ref(false);
const newmodel = ref(null);
const newmodelnumber = ref(null);
const newbrand = ref(null);
const newinvoicenumber = ref(null);
const newinvoicedate = ref(null);
const newprojectstate = ref(null);
const newprojectname = ref(null);
const newProjectOwnerState = ref(false)
const newprojectownername = ref(null)
const newroomname = ref(null);
const newroomstate = ref(null);
const newstagestate = ref(null);
const newstagename = ref(null);
const newsupplierstate = ref(false);
const newsuppliername = ref(null);
const newsupplierrut = ref(null);
const newsupplieraddress = ref(null);
const newunitname = ref(null);
const newunitstate = ref(false);
const project = ref(null);
const projectowner = ref(null)
const projectOptions = ref([]);
const projectOwnersOptions = ref([])
const reception_date = ref(null);
const stage = ref(null);
const stagesOptions = ref([]);
const room = ref(null);
const roomOptions = ref([]);
const maintenanceApply = ref(false);
const supplier = ref(null);
const suppliersOptions = ref([]);
const unit = ref(null);
const unitOptions = ref([]);
const workername1 = ref(null);
const workerrol1 = ref(null);
const workermail1 = ref(null);
const workerphone1 = ref(null);
const workername2 = ref(null);
const workerrol2 = ref(null);
const workermail2 = ref(null);
const workerphone2 = ref(null);
const $q = useQuasar();
const router = useRouter();

const getBrands = () => {
  axios.get("http://localhost:8000/api/brands").then((response) => {
    const brands = response.data;
    brandOptions.value = brands.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getBuildings = () => {
  axios.get("http://localhost:8000/api/buildings").then((response) => {
    const buildings = response.data;
    buildingOptions.value = buildings.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getInvoices = () => {
  axios.get("http://localhost:8000/api/invoices").then((response) => {
    const invoices = response.data;
    invoicesOptions.value = invoices.map((x) => {
      return { id: x.id, name: x.number.toString() };
    });
  });
};

const getInvoicesSupplier = (supplier_id) => {
  axios.get("http://localhost:8000/api/invoices/supplier/"+supplier_id).then((response) => {
    const invoices = response.data;
    invoicesOptions.value = invoices.map((x) => {
      return { id: x.id, name: x.number.toString() };
    });
  });
};

const getModels = () => {
  axios
    .get("http://localhost:8000/api/models/" + brand.value)
    .then((response) => {
      const models = response.data;
      modelOptions.value = models.map((x) => {
        return { id: x.id, name: x.name };
      });
    });
};

const getModelNumbers = () => {
  axios
    .get("http://localhost:8000/api/model_numbers/" + model.value)
    .then((response) => {
      const modelnumbers = response.data;
      modelNumberOptions.value = modelnumbers.map((x) => {
        return { id: x.id, name: x.number };
      });
    });
};

const getProjects = () => {
  axios.get("http://localhost:8000/api/projects").then((response) => {
    const projects = response.data;
    projectOptions.value = projects.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getProjectOwners = () => {
  axios.get("http://localhost:8000/api/project_owners").then((response) => {
    const projectsowners = response.data;
    projectOwnersOptions.value = projectsowners.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getRooms = () => {
  const api_url = "http://localhost:8000/api/rooms/" + unit.value;
  axios.get(api_url).then((response) => {
    room.value = null;
    const rooms = response.data;
    roomOptions.value = rooms.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getStages = () => {
  const api_url = "http://localhost:8000/api/stages/" + project.value;
  axios.get(api_url).then((response) => {
    stage.value = null;
    const stages = response.data;
    stagesOptions.value = stages.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getSuppliers = () => {
  axios.get("http://localhost:8000/api/suppliers").then((response) => {
    const suppliers = response.data;
    suppliersOptions.value = suppliers.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const getUnits = () => {
  const api_url = "http://localhost:8000/api/units/" + building.value;
  axios.get(api_url).then((response) => {
    unit.value = null;
    room.value = null;
    roomOptions.value = [];
    const units = response.data;
    unitOptions.value = units.map((x) => {
      return { id: x.id, name: x.name };
    });
  });
};

const onReset = () => {
  name.value = null;
  serial.value = null;
  inventory.value = null;
  model.value = null;
  maintenance.value = null;
  observation.value = null;
  reception_date.value = null;
};

async function createNewBrand() {
  if (!newbrandstate.value) {
    return brand.value;
  }

  const branddata = {
    name: newbrand.value,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/brands",
      branddata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la marca: " + error,
    });
  }
}

async function createNewBuilding() {
  if (!newbuildingstate.value) {
    return building.value;
  }

  const buildingdata = {
    name: newbuildingname.value,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/buildings",
      buildingdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el edificio: " + error,
    });
  }
}

async function createNewInvoice() {
  if (!newinvoicestate.value) {
    return invoice.value;
  }

  const invoicedata = {
    number: newinvoicenumber.value,
    date: newinvoicedate.value,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/invoices",
      invoicedata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la factura: " + error,
    });
  }
}

async function createNewModel(brand_id) {
  if (!newbrandstate.value && !newmodelstate.value) {
    return model.value;
  }

  const newmodeldata = {
    name: newmodel.value,
    brand_id: brand_id,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/models",
      newmodeldata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el modelo: " + error,
    });
    return -1;
  }
}

async function createNewModelnumber(model_id) {
  if (!newbrandstate.value && !newmodelstate.value && !newmodelnumber.value) {
    return modelNumber.value;
  }

  const newmodelnumberdata = {
    number: newmodelnumber.value,
    model_id: model_id,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/model_numbers",
      newmodelnumberdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el número de modelo: " + error,
    });
  }
}

async function createNewProject(project_owner_id) {
  if (!newprojectstate.value) {
    return project.value;
  }

  const projectname = newprojectname.value;

  if (projectname.trim().length == 0) {
    return -1;
  }

  if (project_owner_id == -1){
    project_owner_id = null
  }

  const projectdata = {
    name: projectname,
    owner_id: project_owner_id
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/projects",
      projectdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el proyecto: " + error,
    });
  }
}

async function createNewProjectOwner() {
  if (!newProjectOwnerState.value) {
    return projectowner.value;
  }

  const projectownername = newprojectownername.value;

  if (projectownername.trim().length == 0) {
    return -1;
  }

  const projectownerdata = {
    name: projectownername,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/project_owners",
      projectownerdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el patrocinador: " + error,
    });
  }
}

async function createNewUnit(building_id) {
  if (!newbuildingstate.value && !newunitstate.value) {
    return unit.value;
  }

  const unitdata = {
    name: newunitname.value,
    building_id: building_id,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/units",
      unitdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la unidad: " + error,
    });
  }
}

async function createNewRoom(unit_id) {
  if (!newbuildingstate.value && !newunitstate.value && !newroomstate.value) {
    return room.value;
  }
  const roomdata = {
    name: newroomname.value,
    unit_id: unit_id,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/rooms",
      roomdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la sala: " + error,
    });
  }
}

async function createNewSupplier() {
  if (!newsupplierstate.value) {
    return supplier.value;
  }
  const supplierdata = {
    name: newsuppliername.value,
    rut: newsupplierrut.value,
    city_address: newsupplieraddress.value,
  };
  try {
    const response = await axios.post(
      "http://localhost:8000/api/suppliers",
      supplierdata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el proveedor: " + error,
    });
  }
}

async function createNewWorker(supplier_id) {
  if (!newsupplierstate.value) {
    return;
  }
  if (workername1.value != null) {
    const workerdata1 = {
      name: workername1.value,
      position: workerrol1.value,
      phone: workerphone1.value,
      email: workermail1.value,
      supplier_id: supplier_id,
    };
    try {
      const response = await axios.post(
        "http://localhost:8000/api/suppliers_contacts",
        workerdata1
      );
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el contacto 1: " + error,
      });
    }
  }
  if (workername2.value != null) {
    const workerdata2 = {
      name: workername2.value,
      position: workerrol2.value,
      phone: workerphone2.value,
      email: workermail2.value,
      supplier_id: supplier_id,
    };
    try {
      const response = await axios.post(
        "http://localhost:8000/api/suppliers_contacts",
        workerdata2
      );
    } catch (error) {
      $q.notify({
        color: "red-3",
        textColor: "white",
        icon: "error",
        message: "No se pudo crear el contacto 2: " + error,
      });
    }
  }
}

async function createNewStage(project_id) {
  if (!newstagestate.value && !newprojectstate.value) {
    return stage.value;
  }

  const stagename = newstagename.value;

  if (stagename.trim().length == 0) {
    return -1;
  }

  const stagedata = {
    name: newstagename.value,
    project_id: project_id,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/api/stages",
      stagedata
    );
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la etapa: " + error,
    });
  }
}

async function createNewEquipment(equipmentdata) {
  try {
    const response = await axios.post(
      "http://localhost:8000/api/equipments",
      equipmentdata
    );
    if (response.status == 201) {
      $q.notify({
        color: "green-4",
        textColor: "white",
        icon: "check",
        message: "Equipo creado con éxito",
      });
    }
    return response.data;
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear el equipo: " + error,
    });
  }
}

async function createNewProjectEquipment(equipment_id, project_id, stage_id) {
  let relationdata = {
    equipment_id: equipment_id,
    project_id: project_id,
    stage_id: stage_id,
  };
  if (
    project_id == -1 ||
    project_id == null ||
    stage_id == -1 ||
    stage_id == null
  ) {
    return;
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/api/equipments_projects",
      relationdata
    );

    if (response.status == 201) {
      $q.notify({
        color: "green-4",
        textColor: "white",
        icon: "check",
        message: "Relación creada con éxito",
      });
    }
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo crear la relacion: " + error,
    });
  }
}

async function uploadInvoiceImage(equipment_id) {
  if (!newinvoicestate.value || invoiceimage.value == null) {
    return;
  }
  const formData = new FormData();
  formData.append("file", invoiceimage.value);
  try {
    const response = await axios.post(
      "http://localhost:8000/api/invoices/" + equipment_id,
      formData
    );
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo guardar la imagen de factura: " + error,
    });
  }
}

async function uploadEquipmentImage(equipment_id) {
  if (equipmentimages.value == null) {
    return;
  }
  equipmentimages.value.forEach((image) => {
    const formData = new FormData();
    formData.append("file", image);
    uploadEquipmentImage2(equipment_id, formData);
  });
}

async function uploadEquipmentImage2(equipment_id, formData) {
  try {
    const response = await axios.post(
      "http://localhost:8000/api/equipments/" + equipment_id,
      formData
    );
  } catch (error) {
    $q.notify({
      color: "red-3",
      textColor: "white",
      icon: "error",
      message: "No se pudo guardar la imagen del equipo: " + error,
    });
  }
}

async function onSubmit() {
  createEquipmentForm.value.resetValidation();
  let equipmentdata = {
    name: name.value,
    serial_number: serial.value,
    umag_inventory_code: inventory.value,
    reception_date: reception_date.value,
    observation: observation.value,
    model_number_id: modelNumber.value,
    supplier_id: supplier.value,
    invoice_id: invoice.value,
    room_id: room.value,
  };

  loading.value = true;
  if (maintenanceApply.value) {
    equipmentdata["maintenance_period"] = maintenance.value;
  }
  const building_id = await createNewBuilding();
  if (building_id == -1) {
    console.log("1");
    loading.value = false;
    return;
  }
  const unit_id = await createNewUnit(building_id);
  if (unit_id == -1) {
    console.log("2");
    loading.value = false;
    return;
  }
  const room_id = await createNewRoom(unit_id);
  if (room_id == -1) {
    console.log("3");
    loading.value = false;
    return;
  }
  equipmentdata["room_id"] = room_id;

  const brand_id = await createNewBrand();
  if (brand_id == -1) {
    console.log("4");
    loading.value = false;
    return;
  }
  const model_id = await createNewModel(brand_id);
  if (model_id == -1) {
    console.log("5");
    loading.value = false;
    return;
  }
  const model_number_id = await createNewModelnumber(model_id);
  if (model_number_id == -1) {
    console.log("6");
    loading.value = false;
    return;
  }

  equipmentdata["model_number_id"] = model_number_id;

  const supplier_id = await createNewSupplier();
  if (supplier_id == -1) {
    console.log("7");
    loading.value = false;
    return;
  }
  equipmentdata["supplier_id"] = supplier_id;
  await createNewWorker(supplier_id);
  const invoice_id = await createNewInvoice();
  if (invoice_id == -1) {
    console.log("8");
    loading.value = false;
    return;
  }
  equipmentdata["invoice_id"] = invoice_id;

  const equipment_id = await createNewEquipment(equipmentdata);
  const project_owner_id = await createNewProjectOwner();
  const project_id = await createNewProject(project_owner_id);
  const stage_id = await createNewStage(project_id);
  await createNewProjectEquipment(equipment_id, project_id, stage_id);
  await uploadEquipmentImage(equipment_id);
  await uploadInvoiceImage(equipment_id);
  loading.value = false;
  //onReset()

  redirectToEquipment(equipment_id.toString());
}

function redirectToEquipment(equipment_id) {
  router.push({ path: equipment_id });
}

onMounted(() => {
  getBrands();
  getInvoices();
  getProjects();
  getProjectOwners();
  getSuppliers();
  getBuildings();
});
</script>

<style>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
