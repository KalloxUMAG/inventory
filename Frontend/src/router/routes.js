const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      {
        path: "/equipments/:id",
        component: () => import("src/pages/Equipment.vue"),
      },
      {
        path: "/equipments/new_equipment",
        component: () => import("src/pages/CreateEquipment.vue"),
      },
      {
        path: "/equipments",
        component: () => import("src/pages/Equipments.vue"),
      },
      {
        path: "/supplies/new_supply",
        component: () => import("src/pages/CreateSupply.vue"),
      },
      {
        path: "/supplies/:id",
        component: () => import("src/pages/Supply.vue"),
      },
      {
        path: "/supplies/lot/:id",
        component: () => import("src/pages/Lot.vue"),
      },
      { path: "/supplies", component: () => import("src/pages/Supplies.vue") },
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
