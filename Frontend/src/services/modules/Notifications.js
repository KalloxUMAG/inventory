import { Notify } from 'quasar'

export function CatchNotifications(status, message) {
  if (status === 403) {
    ErrorNotification('Sesion expirada, favor inciar sesion de nuevo')
    return
  }
  if (status === 200 || status === 201) {
    SuccessNotification(message)
    return
  }
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

function SuccessNotification(message) {
  Notify.create({
    color: 'green-3',
    textColor: 'white',
    icon: 'done',
    message,
  })
}
