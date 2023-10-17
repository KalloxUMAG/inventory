export const menuItems = [
  {
    label: "Dashboard",
    type: "label",
  },
  {
    label: "Inicio",
    icon: "home",
    to: "/",
    exact: true,
    separator: true,
    type: "nav",
  },
  {
    label: "Equipamiento",
    icon: "biotech",
    to: "/equipments",
    exact: false,
    separator: true,
    type: "nav",
  },
  {
    label: "Insumos",
    icon: "science",
    to: "/supplies",
    exact: false,
    separator: true,
    type: "nav",
  },
  {
    label: "Administracion",
    type: "label",
  },
  {
    label: "Agregar usuario",
    icon: "person",
    to: "/createuser",
    exact: true,
    separator: true,
    type: "nav",
  },
];
