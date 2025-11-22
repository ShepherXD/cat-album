<template>
        <v-app-bar color="teal-lighten-2" app>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
            <v-toolbar-title color="white">My Cat Album</v-toolbar-title>
            <v-btn icon="mdi-magnify"></v-btn>
        </v-app-bar>
        <v-main class="pb-8">
                <v-container class="pa-6">
                    <v-row>
                        <v-col v-for="(cat,index) in cats" :key="index" cols="12" md="6">
                            <!-- 猫猫卡片 -->
                            <v-card class="mx-auto pa-4" :cat="cat">
                                
                                    <v-img
                                    class="align-end text-white"
                                    height="300"
                                    :src=cat.img
                                    cover>
                                    </v-img>

                                    <div class="d-flex align-center px-3 py-1"> 
                
                                        <v-card-title class="text-h5 pa-0 mr-4">
                                            {{ cat.name }}
                                        </v-card-title>

                                        <v-card-subtitle class="text-subtitle-1">
                                            {{cat.breed}}
                                        </v-card-subtitle>

                                        <!-- 占位元素 用来把button挤到右边 -->
                                        <v-spacer></v-spacer>

                                        <!-- 点击就打开改猫信息界面 -->
                                        <v-card-actions class="d-flex justify-end pr-0">
                                            <v-btn @click="openModify[index]=true" color="teal-lighten-2" text="Edit"></v-btn>
                                        </v-card-actions>

                                        <v-overlay v-model="openModify[index]" class="align-center justify-center" scroll-strategy="block">
                                            <v-card width="90vw" max-width="800px" rounded="lg">
                                                    <ModifyCatInfo
                                                        :initialCat="cat"
                                                        @submit="(modifiedCat)=>save(modifiedCat,index)"
                                                        @close="openModify[index]=false"
                                                    />

                                            </v-card>
                                        </v-overlay>


                                    </div>

                                    <v-card-text class="py-0">
                                        <div class="text-truncate" style="max-width: 300;">
                                            {{cat.rem}}
                                        </div>
                                    </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-container>    
                 <!-- 隐藏的上传 -->
            <input  type="file" ref="fileInput"  style="display: none" accept="image/*" @change="onFileSelected">
            <!-- 相机&从相册添加按钮 -->
            <v-fab size="large" icon style="position:fixed;bottom: 40px; right: 20px;" z-index="1000" color="light-blue-lighten-1" >
                    <v-icon icon="mdi-camera" color="white"></v-icon>
                    <v-speed-dial v-model="openCameraList" location="top center" transition="slide-y-transition" activator="parent">
                            <v-btn  color="cyan-lighten-1" key="add-btn" icon @click="triggerFileSelected">
                                <v-icon size="24" color="white"  icon="mdi-plus"></v-icon>
                            </v-btn>
                        </v-speed-dial>
            </v-fab>
        </v-main>    
 
</template>

<script setup lang="ts">
import {ref} from 'vue'
import axios from 'axios'
import ModifyCatInfo from './modifyCatInfo.vue'
import {useRouter} from 'vue-router'
import {setTempFile} from '@/utils/store'

const router = useRouter()
const fileInput = ref<HTMLInputElement | null>(null)
const openCameraList = ref(false)
const openModify = ref<Boolean[]>({})
const cats = ref<Cat[]>([
    {name:'花花', breed:'狸花猫', rem:'喜欢咬塑料袋 粘人 可以抱着睡觉wwwwwwwwwwwwwwwwwwwwwwww!', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585595901710366/ee348036bb4ea8951505f81b7eededdf.jpg?ex=69215462&is=692002e2&hm=0b58ebab5dc6b6b18826391b0d355de4cce87a8832d0f156f4b92cb2b32dea92&=&format=webp&width=629&height=653'},
    {name:'黑黑', breed:'黑猫', rem:'特别特别乖的宝宝Q3Q', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585596325072958/6d0006bc62ba976b2b94800833bf8902.jpg?ex=69215462&is=692002e2&hm=80c7979324c803ccea45552c7717944d4d2dd99f8b2b60e68bfdb605a010de18&=&format=webp&width=581&height=653'},
    {name:'小白', breed:'美国短毛猫', rem:'猪~', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585595574550598/f569af35cfa5d9e5d5b12a4daeb41bb9.jpg?ex=69215462&is=692002e2&hm=3859594e52dab32e87c2aaedb610e2321e22a611db32b014823d2b71ea1490e1&=&format=webp&width=869&height=653'}
])

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

const save = (modifiedCat: Cat, index) => {
    cats.value[index] = modifiedCat
    openModify.value[index] = false
    console.log('Modify Success!')
}
export interface Cat {
    id?: number | string; 
    name: string;
    breed: string;
    remark?: string;
    img: string;
}
</script>
<style>

</style>