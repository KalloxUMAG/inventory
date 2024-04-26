<template>
    <div v-if="group != null" class="row justify-center">
        <PageTitle :title="group.name" icon="group">
            <q-btn outline color="secondary" label="Editar" class="floar-right" @click="editGroup"/>
        </PageTitle>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue';
    import {useRoute} from 'vue-router'
    import { sendRequest } from 'src/axios/instance.js'
    
    //Components
    import PageTitle from 'src/components/commons/PageTitle.vue';

    const route = useRoute()
    const id = computed(() => route.params.id)
    const api_prefix = process.env.API_URL;
    const query_groups = api_prefix + "/groups/" + id.value;

    const group = ref(null);

    //Functions
    const editGroup = () => {
        console.log("Edit Group");
    }

    const getGroup = async() => {
        try{
            const response = await sendRequest({
                method: "GET",
                url: query_groups,
            });
            group.value = response.data;
        } catch (error) {
            console.log(error);
        }
    }

    onMounted(() => {
        getGroup();
    });

</script>