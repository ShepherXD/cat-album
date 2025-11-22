<template>

                    <v-sheet color="surface-light" rounded="lg">
                        <v-card class="mx-auto" rounded="lg" >
                            <v-card-title class="d-flex justify-center" >Update Cat Info</v-card-title>
                                <v-card-text style="padding:0.5rem 1rem">
                                    <div class="text-subtitle-1 text-medium-emphasis">Name</div>

                                        <v-text-field
                                            density="compact"
                                            placeholder="Cat's name"
                                            prepend-inner-icon="mdi-cat"
                                            variant="outlined"
                                            v-model="currCat.name"
                                        ></v-text-field>

                                        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                                            Breed

                                            <a class="text-caption text-decoration-none text-blue" href="#" rel="noopener noreferrer"
                                            target="_blank">
                                            Not sure about breed?</a>
                                        </div>

                                        <v-text-field
                                            v-model="currCat.breed"
                                            density="compact"
                                            placeholder="Cat's breed"
                                            prepend-inner-icon="mdi-paw"
                                            variant="outlined"
                                        ></v-text-field>

                                        <div class="text-subtitle-1 text-medium-emphasis">Note</div>

                                        <v-text-field
                                            v-model="currCat.note"
                                            density="compact"
                                            placeholder="Cat's habbit or whatever you want to express"
                                            prepend-inner-icon="mdi-rodent"
                                            variant="outlined"
                                        ></v-text-field>
                                    <!-- <v-text-field
                                    v-model="proxyModel.value"
                                    label="Name"
                                    prepend-icon="$vuetify"
                                    variant="outlined"
                                    ></v-text-field> -->
                                </v-card-text>
                                <v-divider></v-divider>

                                    <v-card-actions>
                                        <v-btn  variant="text" color="deep-orange-lighten-2" @click="$emit('close')">cancel</v-btn>
                                        <v-btn class="flex-grow-1" color="teal-lighten-2" variant="tonal" @click="confirm">save</v-btn>
                                    </v-card-actions>


                        </v-card>
                    </v-sheet>

</template>
<script setup lang="ts">
import {ref,watch} from 'vue'
import type { Cat } from './catAlbum.vue'
const props = defineProps<{
    initialCat: Cat
}>()
console.log('收到的猫:', props.initialCat)
const emit = defineEmits(['close','submit'])
const currCat = ref<Cat | undefined>({})
watch(() => props.initialCat, (newVal) => {
    if(newVal){
        currCat.value = JSON.parse(JSON.stringify(newVal))
    }
}, { immediate: true, deep: true }) //←组件刚创建就执行此监听函数
const confirm = () => {
    emit('submit', currCat.value)
}
</script>