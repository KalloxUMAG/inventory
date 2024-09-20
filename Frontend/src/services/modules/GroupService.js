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

export async function getUsersFromGroup(group_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/user_rol_group/by_group/${group_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los usuarios del grupo')
    return []
  }
}

export async function getUsersNotInGroup(group_id) {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/user_rol_group/not_in_group/${group_id}`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los usuarios no asignados al grupo')
    return []
  }
}

export async function getMyGroups() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/user_rol_group/my_groups`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los grupos del usuario')
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

export async function deleteUserGroupRole(user_id, group_id) {
  try {
    const response = await sendRequest({
      method: 'DELETE',
      url: `${api_prefix}/user_rol_group/${user_id}/${group_id}`,
    })
    CatchNotifications(response.status, 'Usuario eliminado del grupo')
  }
  catch (error) {
    CatchNotifications(error.response.status, 'No se pudo eliminar al usuario del grupo')
  }
}
