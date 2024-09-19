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

export async function getGroupRoles() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/roles`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los roles de grupo')
    return []
  }
}

export async function addUserGroupRole(user_id, group_id, role_id) {
  const data = {
    'user_id': user_id,
    'group_id': group_id,
    'role_id': role_id,
  }
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/user_rol_group`,
      data,
    })
  }
  catch (error) {
    CatchNotifications(error.response.status, 'No se pudo asignar el rol y grupo al usuario')
  }
}
