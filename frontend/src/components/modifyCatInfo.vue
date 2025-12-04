<template>

                    <v-sheet color="surface-light" rounded="0" class="h-100 d-flex">
                        <v-card class="mx-auto flex-grow-1" rounded="0" >
                            <!--TODO: component reuse， distinguish by Update|Add Cat Info-->
                            <v-card-title class="d-flex justify-center pt-8" >{{ mode==='Add' ? 'Add' : 'Edit' }} Cat Info</v-card-title>
                                <v-card-text style="padding:1vh 10vw" >
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

                                            <a class="text-caption text-decoration-none text-blue" href="https://web.archive.org/web/20150111233321/http://www.cfainc.org/Breeds.aspx" rel="noopener noreferrer"
                                            target="_blank">
                                            Not sure about breed?</a>
                                        </div>

                                        <v-text-field
                                            v-model="currCat.breed"
                                            density="compact"
                                            placeholder="Cat's breed"
                                            prepend-inner-icon="mdi-paw"
                                            variant="outlined"
                                            :disabled="isAnalysing"
                                        ></v-text-field>

                                        <div class="text-subtitle-1 text-medium-emphasis">Remark</div>

                                        <v-text-field
                                            v-model="currCat.remark"
                                            density="compact"
                                            placeholder="Whatever you want to remark"
                                            prepend-inner-icon="mdi-rodent"
                                            variant="outlined"
                                        ></v-text-field>

                                        <v-btn v-if="mode === 'Edit'" @click="deleteInfo" width="100%" variant="flat" color="red-lighten-2">Delete</v-btn>
                                </v-card-text>
                                <v-divider></v-divider>

                                    <v-card-actions class="py-8" style="padding-left: 10vw; padding-right: 10vw">
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
    initialCat: Cat | null
    mode: string
    isAnalysing?: Boolean
}>()
console.log('your cat:', props.initialCat)
const emit = defineEmits(['close','submit','delete'])
const currCat = ref<Cat>({})
watch(() => props.initialCat, (newVal) => {
    if(props.mode === 'Edit'){
        if(newVal){
        currCat.value = JSON.parse(JSON.stringify(newVal))
    }}else if (props.mode === 'Add'){
        if (newVal.id) currCat.value.id = newVal.id
        if (newVal.name) currCat.value.name = newVal.name
        if (newVal.breed) currCat.value.breed = newVal.breed
        if (newVal.remark) currCat.value.remark = newVal.remark
    }

}, { immediate: true, deep: true }) //← run when the component is created

// if props.disableBreedEdit is turned into disable, then clear breed field
watch(() => props.isAnalysing, (newVal) => {
    if(newVal){
        currCat.value.breed = "Analysing..."
    }
}, { immediate: true })

const confirm = () => {
    emit('submit', currCat.value)
}

const deleteInfo = () => {
    emit('delete', currCat.value.id)
}
</script>