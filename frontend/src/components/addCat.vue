<template>
  <!-- <v-app-bar v-if="!isEditOpened" color="transparent" elevation="0" absolute>
      <template v-slot:prepend>
        <v-btn icon="mdi-arrow-left" variant="tonal" color="white" class="bg-black-alpha" @click="goBack"></v-btn>
      </template>
  </v-app-bar> -->

  <v-main class="bg-black d-flex flex-column  overflow-hidden" style="height: 100%">
    <v-btn
        icon="mdi-arrow-left"
        variant="text"
        color="white"
        class="position-absolute top-0 left-0 ma-4"
        style="z-index: 10"
        @click="goBack"
    ></v-btn>
    <div class="flex-grow-1 d-flex align-center overflow-hidden justify-center w-100 position-relative"
        :class="{'lifted':isEditOpened}">
        <v-progress-linear :active="isLoading" :indeterminate="isLoading" 
                            color="cyan-darken-1" height="6" absolute location="top" ></v-progress-linear>
        <v-img :src="tempUploadStore.preview" width="100%" @click="visible=true">
            <div class="d-flex fill-height align-end justify-center pb-4">
                 <v-chip :model-value="true" class="ma-2" :class="showChip? 'visible-chip':'invisible-chip'" color="teal-lighten-1" variant="flat" @click.stop>
                    Cat's Breed:  {{ currCat.breed }}
                  <v-icon end icon="mdi-close-circle" @click.stop="hideChip"></v-icon>
                </v-chip>
            </div>
        </v-img>
                
        <!-- <v-snackbar v-model="isSnackBarOpened"   color="teal" rounded="pill" min-width="auto" max-width="80vw" absolute location="top">
          <strong class="text-truncate">Cat's Breed: {{ currCat.breed }}</strong>
        </v-snackbar> -->
         
    </div>

    <input type="file" ref="fileInput" accept="image/*"  style="display: none"  @change="onFileSelected">
    <input type="file" ref="cameraInput" accept="image/*" capture="environment" style="display: none"  @change="onFileSelected">

    <div class="d-flex align-center w-100 pb-10 pt-4 flex-shrink-0" v-if="!isEditOpened">
        
      <div class="d-flex justify-center" style="flex: 1"> 
        <v-btn icon="mdi-replay" @click="opencamera" size="x-large" variant="text" color="white"></v-btn>
      </div>

      <v-btn color="pink-accent-2" @click="checkStatus" size="x-large" icon>
        <v-icon icon="mdi-check"  color="white"></v-icon>
      </v-btn>

      <div class="d-flex justify-center" style="flex: 1">
        <v-btn icon="mdi-close" size="x-large" variant="text" color="white" @click="removeFile"></v-btn>
        <v-btn icon="mdi-pencil" @click="isEditOpened=true" variant="text" size="x-large" color="white"></v-btn>
      </div>

    </div> 


    <v-bottom-sheet v-model="isEditOpened" rounded="0" min-height="50vh" class="overflow-hidden">
      <ModifyCatInfo
        :initial-cat="currCat"
        :mode="'Add'"
        @delete="deleteInfo"
        @submit="(addedCat)=>save(addedCat)"
        @close="isEditOpened=false"/>  <!--sumbit info even when user click 'close' (by accident)-->
    </v-bottom-sheet>
    <!-- go back dialog -->
    <v-dialog v-model="isBackDialogOpened">
      <v-card prepend-icon="mdi-update" max-width="400" class=""
        text="Analysis of cat's breed is in progress.
        Your image will still be saved but may not get result."
        title="Are you sure to go back?">
        
        <template v-slot:actions>
          <v-btn @click="goBack" variant="text">
            Go Back
          </v-btn>

          <v-btn @click="isBackDialogOpened = false" class="flex-grow-1" color="primary" variant="tonal">
            Stay
          </v-btn>
        </template>
    </v-card>
    </v-dialog>
    <!-- retry dialog -->
    <v-dialog v-model="isRetryDialogOpened">
      <v-card prepend-icon="mdi-alert-circle-outline" max-width="400" class=""
        title="Analysis Failed">
        <v-card-text>
          {{ retryText }}
        </v-card-text>
        <template v-slot:actions>
          <v-btn @click="isRetryDialogOpened=false" variant="text">
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
const isEditOpened = ref<Boolean>(false)
const isBackDialogOpened = ref<Boolean>(false)
const isRetryDialogOpened = ref<Boolean>(false)
const currCat = ref<Cat>({})
const mode = ref('Add')
const retryText = ref<String>(null)
const isLoading = ref<Boolean>(false)
const showChip = ref<Boolean>(true)
const isSnackBarOpened = ref<Boolean>(false)
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
        currCat.value.id = res.data.id
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
        isSnackBarOpened.value = true
        clearInterval(pollingTimer)
        pollingTimer = null

        if(currCat.value.breed === 'No Cat'){
          retryText.value = 'There is no cat in the photo. Please upload another cat photo and retry.'
          isRetryDialogOpened.value = true
        }

      } else if(status === 'FAILED'){
        isLoading.value = false
        clearInterval(pollingTimer)
        // alert('Gemini API is overloaded. Please try again later.')
        currCat.value.breed = 'Analysis Failed'
        //should open dialog and let user retry
        retryText.value = "Gemini API is overloaded. Please try again."
        isRetryDialogOpened.value = true
        pollingTimer = null
      }
    })
  }, 750)
}

const checkStatus = () => {
  if (isLoading.value === true){
    isBackDialogOpened.value = true
    console.log(isBackDialogOpened.value)

  } else {
    console.log(isLoading.value)
    console.log(isBackDialogOpened.value)
    goBack()
  }
}

const goBack = () => {
    clearTempFile()
    router.back()
}

//NOTE：run save() nomatter click 'cancel' or 'submit'
const save = (addedCat: Cat, index) => {
    isEditOpened.value = false
    currCat.value = addedCat
    const formData = new FormData()
    formData.append('name', currCat.value.name||"")
    // formData.append('breed', newCat.breed||"")
    formData.append('remark', currCat.value.remark||"")
    axios.patch(`api/cat/${currCat.value.id}`,formData,{
    }).then(function(res){
        console.log('Add Success!,', res.data)
    })
    // clearTempFile()
    // router.back()
}

const hideChip = () => {
    showChip.value = false
}
const retry = (txt: string) => {
    if (txt.match(/overloaded/)) {
      putCat()
      isRetryDialogOpened.value = false

    } else if (txt.match(/no cat/)) {
      isRetryDialogOpened.value = false
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

const removeFile = () => {
  // delete cat image from server via DELETE /cat API
  // then back to previous page
  if (pollingTimer) {
      clearInterval(pollingTimer)
      pollingTimer = null
  }
  if (currentController) {
      currentController.abort()
  }
  if (isLoading.value) {
      isLoading.value = false
  }
  if (currCat.value.id)
  {
    axios.delete(`api/cat/${currCat.value.id}`)
          .then(function(res){
              console.log('Delete temp cat image success')
              goBack()
          }).catch(function(error){
              console.log('Delete temp cat image failed')
              goBack()
        })
  }



}

let themeColor = ref<string>('#000000')

onUnmounted(() => {
    if (currentController) currentController.abort()
    // if (pollingTimer) clearInterval(pollingTimer)
    updateThemeColor(themeColor.value)
})
onMounted(() => {
    themeColor.value = getThemeColor()
    console.log('Stored theme color:', themeColor.value)
    updateThemeColor('#000000')
    
})
const updateThemeColor = (color: string) => {
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) {
        meta.setAttribute('content', color)
    }
}
const getThemeColor = () => {
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) {
        return meta.getAttribute('content')
    }
    return '#FFFFFF'
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
