const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      { path: "/equipments/:id", component: () => import("src/pages/Equipment.vue")},
      { path: "/equipments/new_equipment", component: () => import("src/pages/CreateEquipment.vue")},
      { path: "/equipments", component: () => import("src/pages/Equipments.vue")},
    ],
  },
  //Not found
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
