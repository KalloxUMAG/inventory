import { Cookies } from 'quasar'
import axios from 'axios'

export const reqInstance = axios.create({
  headers: {
    Authorization: `Bearer ${Cookies.get('CATGInventoryToken')}`,
  },
})

export async function sendRequest(config) {
  try {
    const response = await reqInstance(config)
    return response
  }
  catch (error) {
    if (error.response.status === 403) {
      Cookies.remove('CATGInventoryToken')
      Cookies.remove('CATGInventoryFullname')
    }
    throw error
  }
}
