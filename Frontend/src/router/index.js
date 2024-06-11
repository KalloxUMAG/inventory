import { route } from 'quasar/wrappers'
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router'
import { LocalStorage } from 'quasar'
import routes from './routes'

export default route((/* { store, ssrContext } */) => {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  Router.beforeEach((to, from, next) => {
    const token = LocalStorage.getItem('CATGInventoryToken')
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!token)
        next({ name: 'login' })
      else
        next()
    }
    else {
      next()
    }
  })
  return Router
})
