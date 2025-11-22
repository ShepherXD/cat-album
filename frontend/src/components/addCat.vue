<template>
  <v-app>
    <v-app-bar color="transparent" elevation="0" absolute>
      <template v-slot:prepend>
        <v-btn icon="mdi-arrow-left" variant="tonal" color="white" class="bg-black-alpha" @click="$router.back()"></v-btn>
      </template>
    </v-app-bar>
  </v-app>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Cat } from './catAlbum.vue'

const router = useRouter()
const isEditing = ref<Boolean>(false)
const newCat = reactive({
    name: '',
    breed: '',
    remark: ''
})


</script>
