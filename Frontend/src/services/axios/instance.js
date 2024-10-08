import { Cookies } from 'quasar'
import axios from 'axios'

export const reqInstance = axios.create()

// Interceptor para agregar el token en cada solicitud
reqInstance.interceptors.request.use((config) => {
  const token = Cookies.get('CATGInventoryToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}` // Actualiza el header Authorization con el token
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export async function sendRequest(config) {
  try {
    const response = await reqInstance(config)
    return response
  } catch (error) {
    if (error.response && error.response.status === 401) {
      Cookies.remove('CATGInventoryToken')
      Cookies.remove('CATGInventoryFullname')
    }
    throw error
  }
}
