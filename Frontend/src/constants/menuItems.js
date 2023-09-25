export const menuItems = [
  {
    label: "Inicio",
    icon: "home",
    to: "/",
    exact: true,
    separator: true,
  },
  {
    label: "Equipamiento",
    icon: "biotech",
    to: "/equipments",
    exact: false,
    separator: true,
  },
  {
    label: "Insumos",
    icon: "science",
    to: "/supplies",
    exact: false,
    separator: true,
  },
  {
    label: "Agregar usuario",
    icon: "person",
    to: "/createuser",
    exact: true,
    separator: true,
  },
  {
    label: "Gestion",
    icon: "settings",
    to: "/settings",
    exact: true,
    separator: true,
  },
  {
    label: "Cerrar sesion",
    icon: "logout",
    to: "/login",
    exact: true,
    separator: true,
  },
];
