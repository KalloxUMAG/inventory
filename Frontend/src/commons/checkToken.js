import { Cookies } from 'quasar'
import axios from 'axios'

export async function checkToken() {
  const api_prefix = process.env.API_URL
  const key = 'CATGInventoryToken'
  const value = { access_token: Cookies.get(key), token_type: 'nowonder' }
  try {
    const response = await axios.get(`${api_prefix}/users/me/`, value)
    return response
  }
  catch (error) {
  }
}
