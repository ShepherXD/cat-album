import { reactive,ref } from 'vue'

export const tempUploadStore = reactive({
    file: null as File | null,      
    preview: '' as string        
})


export const setTempFile = (file: File) => {
    tempUploadStore.file = file
    // preview url
    if (tempUploadStore.preview) {
        URL.revokeObjectURL(tempUploadStore.preview)
    }
    tempUploadStore.preview = URL.createObjectURL(file)
}


export const clearTempFile = () => {
    tempUploadStore.file = null
    if (tempUploadStore.preview) {
        URL.revokeObjectURL(tempUploadStore.preview)
    }
    tempUploadStore.preview = ''
}


export const deleteConfirm = () => {
    const isDialogOpened = ref<boolean>(false)
    let waiting = null
    const confirm = (): Promise<string> => {
        isDialogOpened.value = true
        return new Promise ((resolve,reject) => {
            waiting = resolve
        })
    }

    const yes = () => {
        isDialogOpened.value = false
        waiting(true)
    }

    const no = () => {
        isDialogOpened.value = false
        waiting(false)
    }

    return {isDialogOpened,confirm, yes, no}
}