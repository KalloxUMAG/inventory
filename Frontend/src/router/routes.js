const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "", component: () => import("pages/IndexPage.vue"), meta: {breadCrumb: [{text: 'Inicio', icon: 'home'}]} },
      {
        path: "/equipments/:id",
        component: () => import("src/pages/Equipment.vue"),
        meta: {breadCrumb(route){ const param = route.currentRoute.value.params.id; return [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Equipamiento', icon: 'biotech', to: '/equipments'}, {text: param}]}},
      },
      {
        path: "/equipments/new_equipment",
        component: () => import("src/pages/CreateEquipment.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Equipamiento', icon: 'biotech', to: '/equipments'}, {text: 'Nuevo Equipo'}]}
      },
      {
        path: "/equipments",
        component: () => import("src/pages/Equipments.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Equipamiento', icon: 'biotech'}]}
      },
      {
        path: "/groups",
        component: () => import("src/pages/groups/List.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Grupos', icon: 'groups'}]}
      },
      {
        path: "/groups/:id",
        component: () => import("src/pages/groups/GroupItemPage.vue"),
        meta: {breadCrumb(route){ const param = route.currentRoute.value.params.id; return [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Grupos', icon: 'groups', to: '/groups'}, {text: param}]}},
      },
      {
        path: "/groups/new_group",
        component: () => import("src/pages/groups/GroupForm.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Grupos', icon: 'groups', to: '/groups'}, {text: 'Nuevo Grupo'}]}
      },
      {
        path: "/supplies/new_supply",
        component: () => import("src/pages/CreateSupply.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Insumos', icon: 'science', to: '/supplies'}]}
      },
      {
        path: "/supplies/:id",
        component: () => import("src/pages/Supply.vue"),
        meta: {breadCrumb(route){ const param = route.currentRoute.value.params.id; return [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Insumos', icon: 'science', to: '/supplies'}, {text: param}]}},
      },
      {
        path: "/supplies/lot/:id",
        component: () => import("src/pages/Lot.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Insumos', icon: 'science', to: '/supplies'}]}
      },
      { 
        path: "/supplies", 
        component: () => import("src/pages/Supplies.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Insumos', icon: 'science'}]}
      },
      {
        path: "/createuser",
        component: () => import("src/pages/CreateUser.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Create User'}]}
      },
      {
        path: "/changepassword",
        component: () => import("src/pages/ChangePassword.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Change Password'}]}
      },
      {
        path: "/inventory-maintainer",
        component: () => import("src/pages/InventoryMaintainer.vue"),
        meta: {breadCrumb: [{text: 'Inicio', icon: 'home',  to: '/'}, {text: 'Mantenedor de inventario', icon: 'calendar_month'}]}
      },
    ],
  },
  {
    path: "/login",
    component: () => import("layouts/LoginLayout.vue"),
    children: [
      { path: "", name: "login", component: () => import("pages/Login.vue") },
    ],
  },
  //Not found
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
