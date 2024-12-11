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

export async function getSupplier(id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers/${id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar el proveedor')
  }
}

export async function getSupplierContacts(id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers_contacts/contacts/${id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los contactos del proveedor')
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

export async function updateSupplier(supplierId, data) {
  try {
    await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/suppliers/${supplierId}`,
      data,
    })
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al actualizar el proveedor')
  }

}

export async function updateSupplierContact(contactId, data) {
  try {
    await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/suppliers_contacts/${contactId}`,
      data,
    })
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al actualizar el contacto del proveedor')
  }
}