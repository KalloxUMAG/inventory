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
