import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useLoanStore = defineStore("loan", {
  actions: {
    async postLoanEquipment(body) {
      try {
        const { data } = await api.post(`inventory/loans`, body);
        return data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },

    async fetchLoan() {
      try {
        const { data } = await api.get(`inventory/loans`);
        return data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },
  },
});
