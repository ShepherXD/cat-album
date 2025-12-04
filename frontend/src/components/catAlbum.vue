<template>
        <v-app-bar :color="isScrolled ? 'transparent' : 'teal-lighten-2'" app>
            <!-- ↑↑↑TODO: app-bar's scroll css ↑↑↑  ↑↑↑-->
            <!-- <v-app-bar-nav-icon @click="openDrawer=!openDrawer"></v-app-bar-nav-icon> -->
            <v-toolbar-title color="white">Cat Album</v-toolbar-title>
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
                <v-container class="px-5 pt-0" fluid>
                    <v-row v-show="showMode.isCard" class="mt-3">
                        <v-col v-for="(cat,index) in cats" :key="cat.id" cols="12" sm="6" md="3">
                        <v-card class="mx-auto" :cat="cat">
                            <!-- <v-skeleton-loader :loading="isLoading" type="image, list-item-two-line"> -->
                            <v-img
                            :src="cat.image_url"
                            height="235px"
                            cover
                            class="align-end text-white"
                            gradient="to bottom, rgba(0,0,0,0) 60%, rgba(0,0,0,0.8) 100%"
                            @click="showImg(index)"
                            >
                                <v-btn
                                    icon="mdi-pencil"
                                    variant="text"
                                    color="white"
                                    size="small"
                                    class="position-absolute top-0 right-0 ma-2"
                                    @click.stop="openModify[cat.id]=true"
                                ></v-btn>

                                <div class="pa-3">
                                    <div class="text-h6 font-weight-bold lh-1">
                                    {{ cat.name }}
                                    </div>
                                    <div class="text-caption opacity-80">
                                    {{ cat.breed }}
                                    </div>
                                </div>
                            </v-img>

                            <v-card-text class="pa-2 d-flex align-center text-caption text-grey-darken-1">
                            <v-icon size="x-small" color="grey" class="mr-1" icon="md:pets"></v-icon>
                                <span class="text-truncate">
                                    {{ cat.remark || '\u00A0' }}
                                </span>
                            </v-card-text>

                            <v-overlay v-model="openModify[cat.id]" class="align-center justify-center" scroll-strategy="block">
                                            <v-card width="90vw" max-width="800px" rounded="lg">
                                                    <ModifyCatInfo
                                                        :initialCat="cat"
                                                        :mode="'Edit'"
                                                        @delete="(id)=>deleteInfo(id,index)"
                                                        @submit="(modifiedCat)=>save(modifiedCat,index)"
                                                        @close="openModify[cat.id]=false"
                                                    />

                                            </v-card>
                            </v-overlay>
                                

                            <!-- </v-skeleton-loader> -->
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row v-show="showMode.isGallery" class="mt-1" >
                        <v-col v-for="(cat, index) in cats" :key="cat.id" cols="4" sm="3" md="2" class="pa-0">
                            <v-img
                            :src="cat.image_url"
                            @click="showImg(index)"
                            aspect-ratio="1"
                            cover
                            style="margin: 1px;"
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
            <v-fab size="large" icon style="position:fixed;bottom: 40px; right: 20px;" z-index="1000" color="pink-accent-2">
                    <v-icon icon="mdi-plus" color="white"></v-icon>
                    <v-speed-dial v-model="openSpeedDial"  location="top center" transition="slide-y-transition" 
                                    activator="parent">
                     <!-- ↑↑↑↑↑ activator="parent" disable click event of fab itself ↑↑↑↑↑ -->
                            <v-btn color="purple-lighten-2" key="camera-btn" icon @click="cameraInput.click()"> 
                                <v-icon size="24" color="white" icon="mdi-camera"></v-icon>
                            </v-btn>
                            <v-btn  color="cyan-lighten-2" key="add-btn" icon @click="fileInput.click()">
                                <v-icon size="24" color="white"  icon="mdi-file-upload"></v-icon>
                            </v-btn>

                        </v-speed-dial>
            </v-fab>
            <!-- delete dialog -->
            <v-dialog v-model="isDialogOpened" max-width="400" >
                <v-card prepend-icon="mdi-alert-circle-outline" class=""
                    title="Are you sure to delete?">
                    <v-card-text>
                        This operation cannot be undone.
                    </v-card-text>
                    <template v-slot:actions>
                        <div class="d-flex w-100">
                            <v-btn @click="no" variant="text" class="w-50">
                                Cancel
                            </v-btn>
                            <v-btn @click="yes" variant="tonal" color="red-lighten-2" class="w-50">
                                Delete
                            </v-btn>
                        </div>

                    </template>
                </v-card>
            </v-dialog>

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
import {setTempFile} from '@/store/store'
import VueEasyLightbox from 'vue-easy-lightbox'
import { deleteConfirm } from '@/store/store'
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
    formData.append('name', modifiedCat.name||"")
    formData.append('breed', modifiedCat.breed||"")
    formData.append('remark', modifiedCat.remark||"")
    axios.patch(`api/cat/${modifiedCat.id}`,formData,{
    }).then(function(res){
        console.log('Modify Success!,', res.data)
    })
}


const {isDialogOpened,confirm, yes,no} = deleteConfirm()
const deleteInfo = async (id: number,index) => {
    const result = await confirm()
    if (result) {
        axios.delete(`api/cat/${id}`)
        .then(function(res){
            const name = res.data.name||'Anonymous'
            cats.value.splice(index,1)
            console.log('Delete Sucess!,',name, 'has left.')
        })

    }else {
        console.log('delete canceled')
    }

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