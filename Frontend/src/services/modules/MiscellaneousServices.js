import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getBrands() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/brands`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar las marcas')
    return []
  }
}

export async function getBuildings() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/buildings`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los edificios')
    return []
  }
}

export async function getInvoices() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/invoices`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar las facturas')
    return []
  }
}

export async function getInvoicesSupplier(supplier_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/invoices/supplier/${supplier_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los proveedores de las facturas')
    return []
  }
}

export async function getModels(brand_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/models/${brand_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los modelos')
    return []
  }
}

export async function getModelNumbers(model_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/model_numbers/${model_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los números de modelo')
    return []
  }
}

export async function getProjects() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/projects`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los proyectos')
    return []
  }
}

export async function getProjectOwners() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/project_owners`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los propietarios de proyectos')
    return []
  }
}

export async function getRooms(unit_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/rooms/${unit_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar las salas')
    return []
  }
}

export async function getStages(project_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/stages/${project_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar las etapas')
    return []
  }
}

export async function getSuppliers() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/suppliers`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los proveedores')
    return []
  }
}

export async function getUnits(building_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/units/${building_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar las unidades')
    return []
  }
}
