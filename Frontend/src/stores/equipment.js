import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'
import { reactive, ref } from 'vue'

export const useEquipmentStore = defineStore('equipment', {
  actions: {
    async fetchEquipmentAvailable({ start_date = null, end_date = null }) {
      try {
        const { data } = await api.get(
          `inventory/get_equipments_with_availability`,
          {
            params: {
              start_date,
              end_date,
            },
          },
        )
        return data
      }
      catch (error) {
        console.log(error)
        return []
      }
    },
  },
})

export const useEquipmentFormStore = defineStore('equipmentForm', () => {
  const equipment = reactive({})

  const redirectTo = ref(null)

  const setEquipment = (data) => {
    equipment.value = data
  }

  const setRedirectTo = () => {
    redirectTo.value = '/equipments/new_equipment'
  }

  const clearEquipmentForm = () => {
    equipment.value = {}
    redirectTo.value = null
  }

  return { clearEquipmentForm, equipment, redirectTo, setEquipment, setRedirectTo }
})
