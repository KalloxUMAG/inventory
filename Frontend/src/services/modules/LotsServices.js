import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'
import { data } from 'autoprefixer'

const api_prefix = process.env.API_URL

export async function getLotsBySupplyId(supply_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/lots/supply/${supply_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los lotes')
    return []
  }
}

export async function getLotsBySupplyAndGroupId(supply_id, group_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/lots/supply/${supply_id}/group/${group_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los lotes')
    return []
  }
}

export async function postLot(lot) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/lots`,
      data: lot,
    })
    if (response.status === 201)
      CatchNotifications(response.status, 'Lote creado correctamente')
    return response.data
  }
  catch (error) {
    console.log(error)
    CatchNotifications(error.response.status, error.response.data)
  }
}

export async function deleteLot(lot_id) {
  try {
    const response = await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/lots/deactive/${lot_id}`,
    })
    if (response.status === 205)
      CatchNotifications(response.status, 'Lote eliminado correctamente')
    return response.data
  }
  catch (error) {
    console.log(error)
    CatchNotifications(error.response.status, error.response.data)
  }
}
