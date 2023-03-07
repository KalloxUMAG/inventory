const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      { path: "/equipment",component: () => import("pages/Equipment.vue")},
      { path: "/suppliers", component: () => import("pages/Suppliers.vue")},
      { path: "/buildings", component: () => import("pages/Buildings.vue")},
      { path: "/projects", component: () => import("pages/Projects.vue")},
      { path: "/form", component: () => import("pages/Form.vue") },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
