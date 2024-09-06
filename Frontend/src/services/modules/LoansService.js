import { sendRequest } from '/src/services/axios/instance.js'
import { CatchNotifications } from './Notifications'

const api_prefix = process.env.API_URL

export async function getLoans() {
  try {
    const response = await sendRequest({
      method: 'GET',
      url: `${api_prefix}/loans`,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los préstamos')
    return []
  }
}

export async function postLoan(loan) {
  try {
    const response = await sendRequest({
      method: 'POST',
      url: `${api_prefix}/loans`,
      data: loan,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al cargar los préstamos')
    return []
  }
}

export async function putLoan(id, loan) {
  try {
    const response = await sendRequest({
      method: 'PUT',
      url: `${api_prefix}/loans/${id}`,
      data: loan,
    })
    return response.data
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al editar el préstamo')
    return []
  }
}

export async function deleteLoan(id) {
  try {
    const response = await sendRequest({
      method: 'DELETE',
      url: `${api_prefix}/loans/${id}`,
    })
    CatchNotifications(response.status, 'Préstamo eliminado correctamente')
  }
  catch (error) {
    CatchNotifications(error.response.status, 'Se ha producido un error al eliminar el préstamo')
    return []
  }
}
