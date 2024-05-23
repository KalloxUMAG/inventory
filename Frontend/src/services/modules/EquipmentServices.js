import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getEquipment(id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/equipments/${id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar el equipo')
  }
}

// GET all equipments in Database without images and maintenances
export async function getEquipments() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/equipments`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los equipos')
    return []
  }
}

export async function getCriticalEquipments() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/equipments/nextmaintenances`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los equipos críticos')
    return []
  }
}

// Maintenances related
export async function getMaintenances(id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/maintenances/${id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar los mantenimientos del equipo')
  }
}

export async function getLastMaintenance(id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/maintenances/last_maintenance/${id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al cargar el ultimo mantenimiento del equipo')
  }
}

export async function postMaintenance(data) {
  try {
    await sendRequest({
      method: 'POST',
      url: `${api_prefix}/maintenances`,
      data,
    })
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al ingresar el mantenimiento')
  }
}

export async function deleteMaintenance(id) {
  try {
    await sendRequest({
      method: 'DELETE',
      url: `${api_prefix}/maintenances/${id}`,
    })
  }
  catch (error) {
    CatchNotifications(error, 'Se ha producido un error al borrar el mantenimiento')
  }
}
