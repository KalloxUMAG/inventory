import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

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
    CatchNotifications(error, 'Se ha producido un error al cargar los insumos')
    return []
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
    CatchNotifications(error, 'Se ha producido un error al cargar los insumos críticos')
    return []
  }
}
