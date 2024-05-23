import { LocalStorage } from 'quasar'
import axios from 'axios'

export const reqInstance = axios.create({
  headers: {
    Authorization: `Bearer ${LocalStorage.getItem('CATGInventoryToken')}`,
  },
})

export async function sendRequest(config) {
  try {
    const response = await reqInstance(config)
    return response
  }
  catch (error) {
    if (error.response.status === 403) {
      LocalStorage.remove('CATGInventoryToken')
      LocalStorage.remove('CATGInventoryFullname')
    }
    throw error
  }
}
