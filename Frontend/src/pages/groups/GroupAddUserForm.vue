<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-md"
      style="width: 900px; max-width: 1000px"
    >
      <q-form ref="AddUserForm" @submit="onOKClick">
        <div class="text-bold text-subtitle1 q-my-sm">
          Agregar Usuario a grupo
        </div>
        <!-- Fields -->
        <div class="col">
          <div class="row q-my-sm">
            <SelectForm
              outlined
              class="col"
              :options="usersOptions"
              option_value="user_id"
              option_label="fullname"
              label="Usuario"
              not_found_label="No hay usuarios disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  user = value;
                }
              "
            />
          </div>
          <div class="row q-my-sm">
            <SelectForm
              outlined
              class="col"
              :options="rolesOptions"
              option_value="id"
              option_label="name"
              label="Rol"
              not_found_label="No hay roles disponibles"
              :rules="[(val) => !!val || 'Campo obligatorio']"
              lazy-rules
              @update-model="
                (value) => {
                  role = value;
                }
              "
            />
          </div>
        </div>
        <!-- Buttons -->
        <div class="q-mt-md row justify-end">
          <q-btn
            color="primary"
            label="Guardar"
            type="submit"
            class="q-mr-sm"
          />
          <q-btn color="negative" label="Cancelar" @click="onDialogCancel" />
        </div>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent, useQuasar } from 'quasar'
import { onMounted, ref } from 'vue'

import SelectForm from 'src/components/SelectForm.vue';

import { addUserGroupRole, getGroupRoles, getUsersNotInGroup } from 'src/services';

defineEmits([...useDialogPluginComponent.emits])

const props = defineProps({
  group_id: Number,
})

const role = ref(null)
const rolesOptions = ref([])
const user = ref(null)
const usersOptions = ref([])

const $q = useQuasar()
const AddUserForm = ref(null)

async function getRoles() {
  rolesOptions.value = await getGroupRoles()
}

async function getUsers() {
  usersOptions.value = await getUsersNotInGroup(props.group_id)
}

onMounted(() => {
  getRoles()
  getUsers()
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()

  async function onOKClick() {
  AddUserForm.value.resetValidation()

  await addUserGroupRole(user.value, props.group_id, role.value)

  onDialogOK()
}
</script>
