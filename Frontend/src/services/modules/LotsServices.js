import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

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
