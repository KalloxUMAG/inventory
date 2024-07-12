import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getGroups() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/groups`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los grupos')
    return []
  }
}
