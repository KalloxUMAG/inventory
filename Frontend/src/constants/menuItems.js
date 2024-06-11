export const menuItems = [
  {
    label: 'Navegación',
    type: 'label',
  },
  {
    label: 'Inicio',
    icon: 'home',
    to: '/',
    exact: true,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Equipamiento',
    icon: 'biotech',
    to: '/equipments',
    exact: false,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Insumos',
    icon: 'science',
    to: '/supplies',
    exact: false,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Proveedores',
    icon: 'store',
    to: '/suppliers',
    exact: false,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Mantenedor de Inventario',
    icon: 'calendar_month',
    to: '/inventory-maintainer',
    exact: false,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Administración',
    type: 'label',
  },
  {
    label: 'Usuarios',
    icon: 'person',
    to: '/users',
    exact: true,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Grupos',
    icon: 'groups',
    to: '/groups',
    exact: true,
    separator: false,
    type: 'nav',
  },
  {
    label: 'Cambiar contraseña',
    icon: 'key',
    to: '/changepassword',
    exact: true,
    separator: false,
    type: 'nav',
  },
]
