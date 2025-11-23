<template>
  <v-app-bar v-if="!openEdit" color="transparent" elevation="0" absolute>
      <template v-slot:prepend>
        <v-btn icon="mdi-arrow-left" variant="tonal" color="white" class="bg-black-alpha" @click="goBack"></v-btn>
      </template>
  </v-app-bar>

  <v-main class="bg-black d-flex flex-column  overflow-hidden" style="height: 100vh">
    <div class="flex-grow-1 d-flex align-center overflow-hidden justify-center w-100 position-relative"
        :class="{'lifted':openEdit}"
        height="60vh">
        <v-progress-linear :active="isLoading" :indeterminate="isLoading" color="cyan-darken-1" height="6" absolute location="top" ></v-progress-linear>
        <v-img :src="tempUploadStore.preview" 
                width="auto" max-width="100%" max-height="90%"></v-img>
        <v-snackbar v-model="openSnackBar" :timeout="2000"  color="teal" rounded="pill" absolute location="top">
          Breed: {{ currCat.breed }}
        </v-snackbar>
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
import { ref,onMounted,onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ModifyCatInfo from './modifyCatInfo.vue'
import axios from 'axios'
import type { Cat } from './catAlbum.vue'
import { tempUploadStore,clearTempFile } from '@/utils/store'

const router = useRouter()
const openEdit = ref<Boolean>(false)
const currCat = ref<Cat>({})
const isLoading = ref<Boolean>(false)
const openSnackBar = ref<Boolean>(false)

onMounted (() => {
  const catImg = tempUploadStore.file
  if(catImg) {
    const formData = new FormData()
    formData.append('image',catImg)
    axios.put('http://localhost:8000/cat', formData,{
    }).then(function(res){
        console.log(res.data)
        const taskid = res.data.analysis_task_id
        if(taskid){
          polling(taskid)
        }
    }).catch(error => { console.log(error) })
  }
})



const polling = (id:number) => {
  isLoading.value = true
  const timer = setInterval(() => {
    axios.get(`http://localhost:8000/cat-breed/task/${id}`)
    .then(function(res){
      const status = res.data.status
      if(status === 'COMPLETED'){
        currCat.value.breed = res.data.result
        console.log(currCat.value.breed)
        isLoading.value = false
        openSnackBar.value = true
        clearInterval(timer)
      } else if(status === 'FAILED'){
        isLoading.value = false
        clearInterval(timer)
        alert('Analysis Failed')
      }
    })
  }, 1000)
}

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
