export const equipmentsColumns = [
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "serial_number",
    align: "left",
    label: "Nro. serie",
    field: "serial_number",
    sortable: false,
  },
  {
    name: "invoice_number",
    align: "left",
    label: "Factura",
    field: "invoice_number",
    sortable: false,
  },
  {
    name: "supplier_name",
    align: "left",
    label: "Proveedor",
    field: "supplier_name",
    sortable: true,
  },
  {
    name: "umag_inventory_code",
    align: "left",
    label: "Inventariado",
    field: "umag_inventory_code",
    sortable: true,
  },
  {
    name: "last_preventive_maintenance",
    align: "left",
    label: "Mantención",
    field: "last_preventive_maintenance",
    sortable: true,
  },
  {
    name: "reception_date",
    align: "left",
    label: "Fecha",
    field: "reception_date",
    sortable: false,
  },
];

export const suppliesColumns = [
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "code",
    align: "left",
    label: "Codigo",
    field: "code",
    sortable: false,
  },
  {
    name: "cost",
    align: "left",
    label: "Costo",
    field: "cost",
    sortable: false,
  },
  {
    name: "supplies_brand_name",
    align: "left",
    label: "Marca",
    field: "supplies_brand_name",
    sortable: true,
  },
  {
    name: "supplies_type_name",
    align: "left",
    label: "Tipo de insumo",
    field: "supplies_type_name",
    sortable: true,
  },
  {
    name: "max_samples",
    align: "left",
    label: "Muestras",
    field: "max_samples",
    sortable: true,
  },
];

export const lotsColumns = [
  {
    name: "supply_name",
    align: "left",
    label: "Insumo",
    field: "supply_name",
    sortable: false,
  },
  {
    name: "supply_code",
    align: "left",
    label: "Codigo",
    field: "supply_code",
    sortable: false,
  },
  {
    name: "number",
    align: "left",
    label: "Lote",
    field: "number",
    sortable: false,
  },
  {
    name: "due_date",
    align: "left",
    label: "Fecha de vencimiento",
    field: "due_date",
    sortable: true,
  },
  {
    name: "location",
    align: "left",
    label: "Localizacion",
    field: "location",
    sortable: true,
  },
  {
    name: "sub_location",
    align: "left",
    label: "Sub-localizacion",
    field: "sub_location",
    sortable: true,
  },
  {
    name: "stock",
    align: "left",
    label: "Stock",
    field: "stock",
    sortable: false,
  },
  {
    name: "supplier_name",
    align: "left",
    label: "Proveedor",
    field: "supplier_name",
    sortable: false,
  },
  {
    name: "observations",
    align: "left",
    label: "Observacion",
    field: "observations",
    sortable: false,
  },
];

export const suppliersColumns = [
  {
    name: "name",
    align: "left",
    label: "Nombre",
    field: "name",
    sortable: false,
  },
  {
    name: "rut",
    align: "left",
    label: "Rut",
    field: "rut",
    sortable: false,
  },
  {
    name: "city_address",
    align: "left",
    label: "Dirección",
    field: "city_address",
    sortable: false,
  }
]

export const rolOptions = [
  {
    value: "Vendedor",
    name: "Vendedor",
  },
  {
    value: "Tecnico",
    name: "Tecnico",
  },
];