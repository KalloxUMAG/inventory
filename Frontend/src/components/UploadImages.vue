<template>
  <q-uploader
    color="blue-6"
    hide-upload-btn
    :max-files="max_files"
    multiple
    accept=".jpg, image/*"
    class="full-width"
    @added="handleAddImages"
    @removed="handleRemoveImages"
  >
    <template v-slot:header="scope">
      <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
        <q-spinner v-if="scope.isUploading" class="q-uploader__spinner" />
        <div class="col">
          <div class="q-uploader__title">{{ label }}</div>
        </div>
        <q-btn
          v-if="scope.canAddFiles"
          type="a"
          icon="add_box"
          @click="scope.pickFiles"
          round
          dense
          flat
        >
          <q-uploader-add-trigger />
          <q-tooltip>Seleccionar imagenes</q-tooltip>
        </q-btn>

        <q-btn
          v-if="scope.isUploading"
          icon="clear"
          @click="scope.abort"
          round
          dense
          flat
        >
          <q-tooltip>Abort Upload</q-tooltip>
        </q-btn>
      </div>
    </template>
    <template v-slot:list="scope">
      <q-list v-if="scope.files.length > 0" separator>
        <q-item v-for="file in scope.files" :key="file.__key">
          <q-item-section>
            <q-item-label class="full-width ellipsis">
              {{ file.name }}
            </q-item-label>

            <q-item-label caption>
              {{ file.__sizeLabel }}
            </q-item-label>
          </q-item-section>

          <q-item-section v-if="file.__img" thumbnail class="gt-xs">
            <img :src="file.__img.src" />
          </q-item-section>

          <q-item-section top side>
            <q-btn
              class="gt-xs"
              size="18px"
              flat
              dense
              round
              icon="delete"
              @click="scope.removeFile(file)"
            />
          </q-item-section>
        </q-item>
      </q-list>
      <div v-else><p>No se han seleccionado imagenes</p></div>
    </template>
  </q-uploader>
</template>

<script setup>
import { toRefs } from "vue";

const props = defineProps({
  label: String,
  max_files: Number,
  handleAddImages: Function,
  handleRemoveImages: Function,
});

const { label, max_files, handleAddImages, handleRemoveImages } = toRefs(props);
</script>
