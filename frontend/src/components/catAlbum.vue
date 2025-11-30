<template>
        <v-app-bar :color="isScrolled ? 'transparent' : 'teal-lighten-2'" app>
            <!-- ↑↑↑TODO: app-bar's scroll css ↑↑↑  ↑↑↑-->
            <v-app-bar-nav-icon @click="openDrawer=!openDrawer"></v-app-bar-nav-icon>
            <v-toolbar-title color="white">My Cat Album</v-toolbar-title>
            <div class="d-flex align-center">
                <v-icon class="mr-2" icon="mdi-card-multiple-outline"></v-icon>
                
                <v-switch 
                    v-model="switchOn" 
                    hide-details 
                    density="compact"
                    base-color="teal-lighten-3"
                    color="cyan-darken-3"
                    @change="changeMode" inset
                ></v-switch>
                
                <v-icon class="mx-2" icon="mdi-image-multiple"></v-icon>
            </div>
        </v-app-bar>

        <v-navigation-drawer
            v-model="openDrawer"
            location="left"temporary>
            <v-list>
                <v-list-item class="pa-2" text-color="grey">
                    <v-icon color="light-blue-darken-1" icon="mdi-magnify"></v-icon>
                    search (coming soon)</v-list-item>
                <v-list-item class="pa-2">
                    <v-icon color="amber-lighten-2" icon="mdi-star-four-points"></v-icon>
                    breeds (coming soon)</v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-main class="pb-8">
                <v-container class="px-3 pt-0">
                    <v-row v-show="showMode.isCard" class="mt-3">
                        <v-col v-for="(cat,index) in cats" :key="cat.id" cols="12" sm="6" md="4">
                            <!-- Cat Cards -->
                            <v-card class="mx-auto pa-4" :cat="cat">
                                <v-skeleton-loader :loading="isLoading" type="image, list-item-two-line">
                                    <v-responsive>
                                        <v-img
                                        class="align-end text-white bg-grey-lighten-2"
                                        height="250"
                                        :src=cat.image_url
                                        @click="showImg(index)"
                                        cover>

                                            <template v-slot:placeholder>
                                                <div class="d-flex align-center justify-center fill-height">
                                                    <v-progress-circular indeterminate color="grey-lighten-4"></v-progress-circular>
                                                </div>
                                            </template>

                                        </v-img>

                                        <div class="d-flex align-center px-3 py-1"> 
                    
                                            <v-card-title class="d-flex flex-shrink-0 text-h6 pa-0 mr-4">
                                                {{ cat.name }}
                                            </v-card-title>

                                            <v-card-subtitle class="d-flex flex-shrink-1 text-subtitle-1 pa-0 text-truncate">
                                                {{cat.breed}}
                                            </v-card-subtitle>
                                
                                            <!-- <v-spacer></v-spacer> -->

                                            <v-card-actions class="d-flex flex-grow-1 flex-shrink-0 justify-end pr-0">
                                                <v-btn @click="openModify[cat.id]=true" color="teal-lighten-2" text="Edit"></v-btn>
                                            </v-card-actions>

                                            <v-overlay v-model="openModify[cat.id]" class="align-center justify-center" scroll-strategy="block">
                                                <v-card width="90vw" max-width="800px" rounded="lg">
                                                        <ModifyCatInfo
                                                            :initialCat="cat"
                                                            @submit="(modifiedCat)=>save(modifiedCat,index)"
                                                            @close="openModify[cat.id]=false"
                                                        />

                                                </v-card>
                                            </v-overlay>
                                        </div>

                                        <v-card-text class="py-0">
                                            <div class="text-truncate" style="max-width: 300;">
                                                {{cat.remark}}
                                            </div>
                                        </v-card-text>
                                    </v-responsive>
                                </v-skeleton-loader>
                                
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row v-show="showMode.isGallery" class="mt-0">
                        <v-col v-for="(cat, index) in cats" :key="cat.id" cols="4" sm="3" md="2" class="pa-0">
                            <v-img
                            :src="cat.image_url"
                            @click="showImg(index)"
                            aspect-ratio="1"
                            cover
                            class="bg-grey-lighten-2 cursor-pointer">
                         
                                <template v-slot:placeholder>
                                    <div class="d-flex align-center justify-center fill-height">
                                        <v-progress-circular indeterminate color="grey-lighten-4"></v-progress-circular>
                                    </div>
                                </template>
            
                            </v-img>
                        </v-col>
                    </v-row>
                </v-container>    
                 <!-- invisible input -->
            <input type="file" ref="cameraInput" accept="image/*" capture="environment" style="display: none"  @change="onFileSelected">
            <input  type="file" ref="fileInput" accept="image/png, image/jpeg, image/jpg" style="display: none" @change="onFileSelected">
            <!-- add from camera & gallery -->
            <v-fab size="large" icon style="position:fixed;bottom: 40px; right: 20px;" z-index="1000" color="light-blue-lighten-1">
                    <v-icon icon="mdi-plus" color="white"></v-icon>
                    <v-speed-dial v-model="openSpeedDial"  location="top center" transition="slide-y-transition" 
                                    activator="parent">
                     <!-- ↑↑↑↑↑ activator="parent" disable click event of fab itself ↑↑↑↑↑ -->
                            <v-btn color="teal-lighten-1" key="camera-btn" icon @click="cameraInput.click()"> 
                                <v-icon size="24" color="white" icon="mdi-camera"></v-icon>
                            </v-btn>
                            <v-btn  color="cyan-lighten-1" key="add-btn" icon @click="fileInput.click()">
                                <v-icon size="24" color="white"  icon="mdi-file-upload"></v-icon>
                            </v-btn>

                        </v-speed-dial>
            </v-fab>
        </v-main>    
        <VueEasyLightbox
            :visible="visible"
            :imgs="catImgUrls"
            :index="index"
            rounded="0"
            @hide="hideImg"></VueEasyLightbox>
</template>

<script setup lang="ts">
import {ref, onMounted,computed} from 'vue'
import axios from 'axios'
import ModifyCatInfo from './modifyCatInfo.vue'
import {useRouter} from 'vue-router'
import {setTempFile} from '@/utils/store'
import VueEasyLightbox from 'vue-easy-lightbox'
const router = useRouter()
const showMode = ref<Object>({
    isGallery: false,
    isCard: true
})
const visible = ref<Boolean>(false)
const index = ref<number>(0)
const fileInput = ref<HTMLInputElement | null>(null)
const cameraInput = ref<HTMLInputElement | null>(null)
const isLoading = ref<Boolean>(true)
const isScrolled = ref<Boolean>(false)
const switchOn = ref<Boolean>(false)
const openSpeedDial = ref<Boolean>(false)
const openModify = ref<Boolean[]>({})
const openDrawer = ref<Boolean>()
const cats = ref<Cat[]>([])
const catImgUrls = computed(() => {
    return cats.value.map(cat => cat.image_url)
})

onMounted (() => {
  axios.get(`api/cat`)
  .then(function(res){
    cats.value = res.data
    console.log('pull success')
    isLoading.value=false
  })
})



const changeMode = () => {
    showMode.value.isCard = !showMode.value.isCard
    showMode.value.isGallery = !showMode.value.isGallery
}

const showImg = (i: number) => {
    index.value = i
    visible.value = true
}

const hideImg = () => {
    visible.value = false
}
const triggerFileSelected = () => {
    fileInput.value.click()
}

const fabStatusChange = (val: boolean) => {
    console.log('fab status changed:', val)
    // if (val === false){
    //     // console.log('I should open camera now!')
    //     cameraInput.value.click()
    // }
}

const onFileSelected = (e: any) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
        setTempFile(selectedFile)
        router.push('/add-cat')
        e.target.value = ''
    }
}

const save = (modifiedCat: Cat, index:number) => {
    cats.value[index] = modifiedCat
    openModify.value[modifiedCat.id] = false

    const formData = new FormData()
    formData.append('name', modifiedCat.name)
    formData.append('breed', modifiedCat.breed)
    formData.append('remark', modifiedCat.remark)
    axios.patch(`api/cat/${modifiedCat.id}`,formData,{
    }).then(function(res){
        console.log('Modify Success!,', res.data)
    })
}
export interface Cat {
    id?: number | string; 
    name: string;
    breed: string;
    remark?: string;
    image_url: string;
}
</script>
<style>

</style>