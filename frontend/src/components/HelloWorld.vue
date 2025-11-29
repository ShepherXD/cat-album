<template>
  <v-container class="fill-height" max-width="900">
    <v-card class="mx-auto" prepend-icon="$vuetify" width="400">
      <template v-slot:title>
        <span class="font-weight-black">Get Today's Cats Name</span>
      </template>

      <v-card-text class="bg-surface-light pt-4">

        <v-btn @click="getCatName" v-if="catName===''">
          Get!
        </v-btn>

        <v-chip class="ml-1" v-if="catName!==''">
          {{catName}}
        </v-chip>
      </v-card-text>
    </v-card>

    <v-card class="mx-auto" prepend-icon="$vuetify" width="400">
      <template v-slot:title>
        <span class="font-weight-black">Get Cats' Breed</span>
    
      </template>

      <v-card-text class="bg-surface-light pt-4">
        <v-form>
          <v-file-input @change="postCatImg" label="File input" density="compact"></v-file-input>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import axios from 'axios';
const catName = ref("");

const catBreed = ref("");

const getCatName = () => {
  const date = "11-17"
  axios.get(`api/cat-name?date=${date}`)
  .then(function(res){
    catName.value = res.data
  })
}


const postCatImg = (e: any) =>{
  if (!e.target.files){
    console.log("没有文件嗷")
    return
  }
  const formData =  new FormData()
  let catImg = e.target.files[0]
  formData.append('catImg',catImg)
  axios.post(`api/cat-breed`, formData,{
  }).then(function(res){
    catBreed.value=res.data
    console.log(catBreed.value)
  })
}

</script>
