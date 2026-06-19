import axios from 'axios'

const api= axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

export function getDocuments(){
    return api.get('/documents/')
}

export function uploadDocument(file: File){
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/documents/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function deleteDocument(id: number){
    return api.delete(`/documents/${id}/`)
}

export function queryChat(question: string, document_id: number){
    return api.post('/chat/query/', { question, document_id })
}