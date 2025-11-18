<template>
  <v-container class="fill-height" max-width="900">
    <v-card
    class="mx-auto"
    prepend-icon="$vuetify"
    width="400"
  >
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
  </v-container>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import axios from 'axios';
const catName = ref("");

function getCatName(){
  const date = "11/17"
  axios.get(`http://localhost:8000/cat-name?date=${date}`)
  .then(function(res){
    console.log(res.data)

  })
  
}

</script>
