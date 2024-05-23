import { Notify } from 'quasar'

export function CatchNotifications(error, message) {
  if (error.response.status === 403)
    ErrorNotification('Sesion expirada, favor inciar sesion de nuevo')
  else
    ErrorNotification(`Se ha producido un error: ${message}`)
}

function ErrorNotification(message) {
  Notify.create({
    color: 'red-3',
    textColor: 'white',
    icon: 'error',
    message,
  })
}
