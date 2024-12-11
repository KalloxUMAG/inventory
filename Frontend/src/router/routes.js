const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/IndexPage.vue'), meta: { breadCrumb: [{ text: 'Inicio', icon: 'home' }] } },
      {
        path: '/equipments/:id',
        component: () => import('src/pages/equipments/EquipmentItemPage.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Equipamiento', icon: 'biotech', to: '/equipments' }, { text: param }] } },
      },
      {
        path: '/equipments/edit/:id',
        component: () => import('src/pages/equipments/EquipmentEditForm.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Equipamiento', icon: 'biotech', to: '/equipments' }, { text: 'Editar' }, { text: param }] } },
      },
      {
        path: '/equipments/new_equipment',
        component: () => import('src/pages/equipments/EquipmentForm.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Equipamiento', icon: 'biotech', to: '/equipments' }, { text: 'Nuevo Equipo' }] },
      },
      {
        path: '/equipments',
        component: () => import('src/pages/equipments/EquipmentList.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Equipamiento', icon: 'biotech' }] },
      },
      {
        path: '/groups',
        component: () => import('src/pages/groups/List.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Grupos', icon: 'groups' }] },
      },
      {
        path: '/groups/:id',
        component: () => import('src/pages/groups/GroupItemPage.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Grupos', icon: 'groups', to: '/groups' }, { text: param }] } },
      },
      {
        path: '/groups/edit/:id',
        component: () => import('src/pages/groups/GroupEditForm.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Grupos', icon: 'groups', to: '/groups' }, { text: 'Editar' }, { text: param }] } },
      },
      {
        path: '/groups/new_group',
        component: () => import('src/pages/groups/GroupForm.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Grupos', icon: 'groups', to: '/groups' }, { text: 'Nuevo Grupo' }] },
      },
      {
        path: '/supplies/new_supply',
        component: () => import('src/pages/CreateSupply.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Insumos', icon: 'science', to: '/supplies' }] },
      },
      {
        path: '/supplies/:id',
        component: () => import('src/pages/supplies/SupplyItemPage.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Insumos', icon: 'science', to: '/supplies' }, { text: param }] } },
      },
      {
        path: '/supplies/lot/:id',
        component: () => import('src/pages/Lot.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Insumos', icon: 'science', to: '/supplies' }] },
      },
      {
        path: '/supplies',
        component: () => import('src/pages/Supplies.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Insumos', icon: 'science' }] },
      },
      {
        path: '/suppliers/new_supplier',
        component: () => import('src/pages/suppliers/SupplierForm.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Proveedores', icon: 'store', to: '/suppliers' }, { text: 'Nuevo Proveedor', icon: 'add_business' }] },
      },
      {
        path: '/suppliers/:id',
        component: () => import('src/pages/suppliers/SupplierItemPage.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Proveedores', icon: 'store', to: '/suppliers' }, { text: param }] } },
      },
      {
        path: '/suppliers',
        component: () => import('src/pages/suppliers/SupplierList.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Proveedores', icon: 'store' }] },
      },
      {
        path: '/users',
        component: () => import('src/pages/users/UserList.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Usuarios', icon: 'person' }] },
      },
      {
        path: '/users/:id',
        component: () => import('src/pages/users/UserItemPage.vue'),
        meta: { breadCrumb(route) { const param = route.currentRoute.value.params.id; return [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Usuarios', icon: 'person', to: '/users' }, { text: param }] } },
      },
      {
        path: '/users/new_user',
        component: () => import('src/pages/users/UserForm.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Usuarios', icon: 'person', to: '/users' }, { text: 'Nuevo Usuario', icon: 'person_add' }] },
      },
      {
        path: '/changepassword',
        component: () => import('src/pages/ChangePassword.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Change Password' }] },
      },
      {
        path: '/loans',
        component: () => import('src/pages/Loans.vue'),
        meta: { breadCrumb: [{ text: 'Inicio', icon: 'home', to: '/' }, { text: 'Prestamos', icon: 'calendar_month' }] },
      },
    ],
  },
  {
    path: '/login',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: '', name: 'login', component: () => import('pages/Login.vue') },
    ],
  },
  // Not found
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
