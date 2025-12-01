<template>
  <v-app-bar v-if="!openEdit" color="transparent" elevation="0" absolute>
      <template v-slot:prepend>
        <v-btn icon="mdi-arrow-left" variant="tonal" color="white" class="bg-black-alpha" @click="goBack"></v-btn>
      </template>
  </v-app-bar>

  <v-main class="bg-black d-flex flex-column  overflow-hidden" style="height: 100%">
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

    <input type="file" ref="fileInput" accept="image/*"  style="display: none"  @change="onFileSelected">
    <input type="file" ref="cameraInput" accept="image/*" capture="environment" style="display: none"  @change="onFileSelected">

    <div class="d-flex justify-space-around align-center w-100 pb-10 pt-4 flex-shrink-0" v-if="!openEdit">
        
      <div> 
        <v-btn icon="mdi-camera" @click="opencamera" size="x-large" variant="text" color="white"></v-btn>
      </div>

      <v-btn color="teal-lighten-2" @click="checkStatus" size="x-large" icon>
        <v-icon icon="mdi-check"  color="white"></v-icon>
      </v-btn>

      <div>
        <v-btn v-if="mode!='Add'" icon="mdi-pencil" @click="openEdit=true" variant="text" size="x-large" color="white"></v-btn>
      </div>

    </div> 


    <v-bottom-sheet v-model="openEdit" rounded="0" min-height="50vh" class="overflow-hidden">
      <ModifyCatInfo
        :initial-cat="currCat"
        :mode="'Add'"
        @delete="deleteInfo"
        @submit="(currCat)=>save(currCat)"
        @close="(currCat)=>save(currCat)"/>  <!--sumbit info even when user click 'close' (by accident)-->
    </v-bottom-sheet>
    <!-- go back dialog -->
    <v-dialog v-model="openBackDialog">
      <v-card prepend-icon="mdi-update" max-width="400" class=""
        text="Analysis of cat's breed is in progress.
        Your image will still be saved but may not get result."
        title="Are you sure to go back?">
        
        <template v-slot:actions>
          <v-btn @click="goBack" variant="text">
            Go Back
          </v-btn>

          <v-btn @click="openBackDialog = false" class="flex-grow-1" color="primary" variant="tonal">
            Stay
          </v-btn>
        </template>
    </v-card>
    </v-dialog>
    <!-- retry dialog -->
    <v-dialog v-model="openRetryDialog">
      <v-card prepend-icon="mdi-alert-circle-outline" max-width="400" class=""
        title="Analysis Failed">
        <v-card-text>
          {{ retryText }}
        </v-card-text>
        <template v-slot:actions>
          <v-btn @click="openRetryDialog=false" variant="text">
            Cancel
          </v-btn>

          <v-btn @click="retry(retryText)" class="flex-grow-1" color="primary" variant="tonal">
            Retry
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
import { tempUploadStore, setTempFile, clearTempFile } from '@/store/store'
import VueEasyLightbox from 'vue-easy-lightbox'

const router = useRouter()
const openEdit = ref<Boolean>(false)
const openBackDialog = ref<Boolean>(false)
const openRetryDialog = ref<Boolean>(false)
const currCat = ref<Cat>({})
const retryText = ref<String>(null)
const isLoading = ref<Boolean>(false)
const showChip = ref<Boolean>(true)
const openSnackBar = ref<Boolean>(false)
const visible = ref<Boolean>(false)  //whole picture
const fileInput = ref<HTMLInputElement | null>(null)
const cameraInput = ref<HTMLInputElement | null>(null)
let currentController: AbortController | null = null 
let pollingTimer = null

onMounted (() => {
    putCat()
})

const putCat = () => {
  if (!showChip.value) {
    showChip.value = true
  }

  if (currentController) {
    currentController.abort()
  }

  currentController =  new AbortController()
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
  const catImg = tempUploadStore.file

  if(catImg) {
    currCat.value.breed = "Analysing..."
    const formData = new FormData()
    formData.append('image',catImg)
    isLoading.value = true
    axios.put('api/cat', formData,{
      signal: currentController.signal
    }).then(function(res){
        console.log(res.data)
        const taskid = res.data.analysis_task_id
        if(taskid){
          polling(taskid)
        }
    }).catch(error => { 
        if(axios.isCancel(error)){
          console.log('privior request cancel')

        }else {
          console.log(error)
        }
    })

  }else {
    currCat.value.breed = "Waiting for cat photo..."
  }
}

const polling = (id:number) => {
  
  pollingTimer = setInterval(() => {
    axios.get(`api/cat-breed/task/${id}`)
    .then(function(res){
      const status = res.data.status
      if(status === 'COMPLETED'){
        currCat.value.breed = res.data.result
        if (!showChip.value) {
          showChip.value = true
        }
        console.log(currCat.value.breed)
        isLoading.value = false
        openSnackBar.value = true
        clearInterval(pollingTimer)
        pollingTimer = null

        if(currCat.value.breed === 'No Cat'){
          retryText.value = 'There is no cat in the photo. Please upload another cat photo and retry.'
          openRetryDialog.value = true
        }

      } else if(status === 'FAILED'){
        isLoading.value = false
        clearInterval(pollingTimer)
        // alert('Gemini API is overloaded. Please try again later.')
        currCat.value.breed = 'Analysis Failed'
        //should open dialog and let user retry
        retryText.value = "Gemini API is overloaded. Please try again."
        openRetryDialog.value = true
        pollingTimer = null
      }
    })
  }, 1000)
}

const checkStatus = () => {
  if (isLoading.value === true){
    openBackDialog.value = true
    console.log(openBackDialog.value)

  } else {
    console.log(isLoading.value)
    console.log(openBackDialog.value)
    goBack()
  }
}

const goBack = () => {
    clearTempFile()
    router.back()
}

//NOTE：run save() nomatter click 'cancel' or 'submit'
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
const retry = (txt: string) => {
    if (txt.match(/overloaded/)) {
      putCat()
      openRetryDialog.value = false

    } else if (txt.match(/no cat/)) {
      openRetryDialog.value = false
      fileInput.value.click()     // openFile(from gallery or take a photo)
      currCat.value.breed = 'Waiting for cat photo...'
    }
    
}

const opencamera = () => {
    cameraInput.value.click()

}

const onFileSelected = (e: any) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
        setTempFile(selectedFile)
        putCat()
        e.target.value = ''
    }
    
}



onUnmounted(() => {
    if (currentController) currentController.abort()
    // if (pollingTimer) clearInterval(pollingTimer)
})

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
