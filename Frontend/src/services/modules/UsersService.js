import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function postUser(data) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/users`,
      data,
    })
    CatchNotifications(response.status, 'Usuario creado con éxito')
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'No se pudo crear el usuario')
  }
}
