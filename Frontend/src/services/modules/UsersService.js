import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getMe() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/users/me`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'No se pudo obtener información del usuario')
  }
}

export async function getUserImage(user_id) {
  const img_url = `${api_prefix}/users/images/`
  try {
    const response = await sendRequest({
      method: 'GET',
      url: img_url + user_id,
    })
    return response.data[0].path
  }
  catch (error) {
    return null
  }
}


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

