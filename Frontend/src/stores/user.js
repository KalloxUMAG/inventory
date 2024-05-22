import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useUserStore = defineStore('user', {
  actions: {
    async fetchUser({ fullname = null, email = null }) {
      try {
        const { data } = await api.get(`users/search_users`, {
          params: {
            fullname,
            email,
          },
        })
        return data
      }
      catch (error) {
        console.log(error)
        return []
      }
    },
  },
})
