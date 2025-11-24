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
        <v-progress-linear :active="isLoading" :indeterminate="isLoading" 
                            color="cyan-darken-1" height="6" absolute location="top" ></v-progress-linear>
        <v-img :src="tempUploadStore.preview" cover @click="visible=true"></v-img>
                
        <!-- <v-snackbar v-model="openSnackBar"   color="teal" rounded="pill" min-width="auto" max-width="80vw" absolute location="top">
          <strong class="text-truncate">Cat's Breed: {{ currCat.breed }}</strong>
        </v-snackbar> -->
         
    </div>
    <div class="text-center flex-shrink-0">
        <v-chip :model-value="true" class="ma-2" :class="showChip? 'visible-chip':'invisible-chip'" color="cyan-darken-1" variant="flat" 
                absolute location="bottom">
            Cat's Breed:  {{ currCat.breed }}
          <v-icon end icon="mdi-close-circle" @click.stop="hideChip"></v-icon>
        </v-chip>
    </div>
    
    <input type="file" ref="cameraInput" accept="image/*" capture="environment" style="display: none"  @change="onFileSelected">

    <div class="d-flex justify-space-around align-center w-100 pb-10 pt-4 flex-shrink-0" v-if="!openEdit">
        
      <div> 
        <v-btn icon="mdi-camera" @click="cameraInput.click()" size="x-large" variant="text" color="white"></v-btn>
      </div>

      <v-btn color="teal-lighten-2" @click="checkStatus" size="x-large" icon>
        <v-icon icon="mdi-check"  color="white"></v-icon>
      </v-btn>

      <div>
        <v-btn icon="mdi-pencil" @click="openEdit=true" variant="text" size="x-large" color="white"></v-btn>
      </div>

    </div> 


    <v-bottom-sheet v-model="openEdit" rounded="0" min-height="50vh" class="overflow-hidden">
      <ModifyCatInfo
        :initial-cat="currCat"
        @submit="(currCat)=>save(currCat)"
        @close="(currCat)=>save(currCat)"/>  <!--象征性按钮-->
    </v-bottom-sheet>
    
    <v-dialog v-model="openDialog">
      <v-card prepend-icon="mdi-update" max-width="400" class=""
        text="Analysis of cat's breed is in progress.
        Your image will still be saved but may not get result."
        title="Are you sure to leave?">
        
        <template v-slot:actions>
          <v-btn @click="goBack" variant="text">
            Leave
          </v-btn>

          <v-btn @click="openDialog = false" class="flex-grow-1" color="primary" variant="tonal">
            Cancel
          </v-btn>
        </template>
    </v-card>
    </v-dialog>

  </v-main>
  <VueEasyLightbox
            :visible="visible"
            :imgs="tempUploadStore.preview"
            rounded="0"
            @hide="visible=false"></VueEasyLightbox>
</template>
<script setup lang="ts">
import { ref,onMounted,onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ModifyCatInfo from './modifyCatInfo.vue'
import axios from 'axios'
import type { Cat } from './catAlbum.vue'
import { tempUploadStore, setTempFile, clearTempFile } from '@/utils/store'
import VueEasyLightbox from 'vue-easy-lightbox'

const router = useRouter()
const openEdit = ref<Boolean>(false)
const openDialog = ref<Boolean>(false)
const currCat = ref<Cat>({
  breed: 'Analysising...'
})
const isLoading = ref<Boolean>(false)
const showChip = ref<Boolean>(true)
const openSnackBar = ref<Boolean>(false)
const visible = ref<Boolean>(false)  //whole picture
const cameraInput = ref<HTMLInputElement | null>(null)

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
        alert('Analysis Failed. Please try again.')
      }
    })
  }, 1000)
}

const checkStatus = () => {
  if (isLoading.value === true){
    openDialog.value = true
    console.log(openDialog.value)
  } else {
    console.log(isLoading.value)
    console.log(openDialog.value)
    goBack()
  }
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
    // clearTempFile()
    // router.back()
}

const hideChip = () => {
  showChip.value = false
}

const onFileSelected = (e: any) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
        setTempFile(selectedFile)
        
        e.target.value = ''
    }
}

</script>
<style scoped>
.lifted {
  transform: translateY(-26vh);
}

.visible-chip {
  visibility: visible;
}

.invisible-chip {
  visibility: hidden; 
}
</style>
