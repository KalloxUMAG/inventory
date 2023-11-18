import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useEquipmentStore = defineStore("equipment", {
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
          }
        );
        return data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },
  },
});
