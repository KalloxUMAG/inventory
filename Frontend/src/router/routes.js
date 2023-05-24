const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      { path: "/equipments/:id", component: () => import("src/pages/Equipment.vue")},
      { path: "/equipments/new_equipment", component: () => import("src/pages/CreateEquipment.vue")},
      { path: "/equipments", component: () => import("src/pages/Equipments.vue")},
      { path: "/supplies/new_supply", component: () => import("src/pages/CreateSupply.vue")},
      { path: "/supplies/new_lot", component: () => import("src/pages/CreateLot.vue")},
      { path: "/supplies/:id", component: () => import("src/pages/Supply.vue")},
      { path: "/supplies/lot/:id", component: () => import("src/pages/Lot.vue")},
      { path: "/supplies", component: () => import("src/pages/Supplies.vue")},
    ],
  },
  //Not found
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
