import { sendRequest } from '/src/services/axios/instance.js'
import { Notify } from 'quasar'

const api_prefix = process.env.API_URL

export async function getSupplies() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies`,
    })
    return response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock
      supply.critical = supply.stock <= supply.critical_stock
      return supply
    })
  }
  catch (error) {
    if (error.respose.status === 403) {
      Notify.create({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: 'Sesion expirada, favor inciar sesion de nuevo',
      })
    }
    Notify.create({
      color: 'red-3',
      textColor: 'white',
      icon: 'error',
      message: 'Se ha producido un error al cargar los equipos',
    })
  }
}

export async function getCriticalSupplies() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/supplies/critical`,
    })
    return response.data.map((supply) => {
      supply.max_samples = supply.samples * supply.stock
      return supply
    })
  }
  catch (error) {
    if (error.respose.status === 403) {
      Notify.create({
        color: 'red-3',
        textColor: 'white',
        icon: 'error',
        message: 'Sesion expirada, favor inciar sesion de nuevo',
      })
      return []
    }
    return []
  }
}
