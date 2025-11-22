<template>
  <v-app-bar v-if="!openEdit" color="transparent" elevation="0" absolute>
      <template v-slot:prepend>
        <v-btn icon="mdi-arrow-left" variant="tonal" color="white" class="bg-black-alpha" @click="goBack"></v-btn>
      </template>
  </v-app-bar>

  <v-main class="bg-black d-flex flex-column  overflow-hidden" style="height: 100vh">
    <div class="flex-grow-1 d-flex align-center overflow-hidden justify-center w-100"
        :class="{'lifted':openEdit}"
        height="60vh">
        <v-img :src="tempUploadStore.preview" 
                width="auto" max-width="100%" max-height="90%"></v-img>
    </div>
    
    <div class="text-center pb-10 flex-shrink-0">
      <v-btn v-if="!openEdit" color="teal-lighten-2" icon="mdi-pencil" size="large" @click="openEdit=true"></v-btn>
    </div>

    <v-bottom-sheet v-model="openEdit" rounded="0" min-height="50vh" class="overflow-hidden">
      <ModifyCatInfo
        :initial-cat="currCat"
        @submit="(currCat)=>save(currCat)"
        @close="(currCat)=>save(currCat)"/>  <!--象征性按钮-->
    </v-bottom-sheet>
    
  </v-main>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ModifyCatInfo from './modifyCatInfo.vue'
import type { Cat } from './catAlbum.vue'
import { tempUploadStore,clearTempFile } from '@/utils/store'

const router = useRouter()
const openEdit = ref<Boolean>(false)
const currCat = ref<Cat>({})

const goBack = () => {
clearTempFile()
console.log("已清除图片链接")
router.back()
}

//NOTE：不管按钮点save还是cancel都会执行save函数
//NOTE: 应该还有个参数，判断是照片来自相册还是来自相机，前者back到猫相册界面，后者back到相机？
//前提是照相界面能内置，只能打开系统相机的话还是都back到猫相册界面
const save = (currCat: Cat, index) => {
    const newCat = currCat
    console.log(newCat)
    console.log('Save Success!')
    openEdit.value = false
    clearTempFile()
    router.back()
}

</script>
<style scoped>
.lifted {
  transform: translateY(-26vh);
}
</style>
