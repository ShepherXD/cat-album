import { reactive } from 'vue'

export const tempUploadStore = reactive({
    file: null as File | null,      
    preview: '' as string        
})


export const setTempFile = (file: File) => {
    tempUploadStore.file = file
    // 预览链接
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