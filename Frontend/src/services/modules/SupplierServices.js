import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getSuppliersFull() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers/full`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los proveedores')
  }
}

export async function postSupplier(data) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/suppliers`,
      data,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al ingresar los proveedores')
  }
}

export async function postSupplierContact(data) {
  try {
    await sendRequest({
      method: 'POST',
      url: `${api_prefix}/suppliers_contacts`,
      data,
    })
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al guardar el contacto del proveedor')
  }
}
