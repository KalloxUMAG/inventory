<template>
    <q-table
        class="q-mt-md" 
        title="productos"
        no-data-label="Sin productos para mostrar"
        :columns="columns"
        :rows="productos"
    />
</template>

<script>

const columns = [ 
    {
        name: 'producto',
        label: 'Producto',
        align: 'left',
        field: 'producto',
        sortable: true
    },
    {
        name: 'prioridad',
        label: 'Prioridad',
        align: 'left',
        field: 'prioridad',
        sortable: true
    }
]

const rows = [
    {
        producto: 'producto 1',
        prioridad: 'maxima'
    },
    {
        producto: 'producto 2',
        prioridad: 'minima'
    }
]

export default {
    props: {
        productos: Array
    },
    
    setup(){
        return{
            columns,
            rows
        }
    }
}
</script>