<template>
    <v-container>
        <v-row>
            <v-col v-for="(cat,index) in cats" :key="index" cols="12" md="6">
                <v-card class="mx-auto" :cat="cat">
                    <v-card-item>
                        <v-img
                        class="align-end text-white"
                        height="300"
                        :src=cat.img
                        cover>
                        <v-card-title>
                            12345
                        </v-card-title>
                        </v-img>

                        <v-card-subtitle class="pt-4">
                        {{ cat.breed }}
                        </v-card-subtitle>

                        <v-card-text >
                            <div class="text-truncate" style="max-width: 300;">
                                {{cat.note}}
                            </div>
                        </v-card-text>

                        <v-card-actions>
                        <v-btn color="orange" text="Edit"></v-btn>
                        </v-card-actions>
                    </v-card-item>

                </v-card>
            </v-col>
        </v-row>

    </v-container>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import axios from 'axios'
const cats = ref([
    {name:'花花', breed:'狸花猫', note:'喜欢咬塑料袋 粘人 可以抱着睡觉wwwwwwwwwwwwwwwwwwwwwwww!', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585595901710366/ee348036bb4ea8951505f81b7eededdf.jpg?ex=69215462&is=692002e2&hm=0b58ebab5dc6b6b18826391b0d355de4cce87a8832d0f156f4b92cb2b32dea92&=&format=webp&width=629&height=653'},
    {name:'黑黑', breed:'黑猫', note:'宝宝', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585596325072958/6d0006bc62ba976b2b94800833bf8902.jpg?ex=69215462&is=692002e2&hm=80c7979324c803ccea45552c7717944d4d2dd99f8b2b60e68bfdb605a010de18&=&format=webp&width=581&height=653'},
    {name:'小白', breed:'美国短毛猫', note:'猪~', img:'https://media.discordapp.net/attachments/1256264823050862622/1440585595574550598/f569af35cfa5d9e5d5b12a4daeb41bb9.jpg?ex=69215462&is=692002e2&hm=3859594e52dab32e87c2aaedb610e2321e22a611db32b014823d2b71ea1490e1&=&format=webp&width=869&height=653'}
])
</script>