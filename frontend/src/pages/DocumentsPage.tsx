import { useState, useEffect} from 'react'
import { getDocuments, uploadDocument, deleteDocument } from '../services/api'
import { useNavigate, Link } from 'react-router-dom'
import duck from '../assets/duck.png'
import type { Document } from '../types'
import DocumentCard from '../components/DocumentsCard'
import Footer from '../components/Down'


function DocumentsPage() {
    const [documents, setDocuments] = useState<Document[]>([])
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const [isDragging, setIsDragging] = useState(false)
    const fetchDocuments = async () => {
        setLoading(true)
        try {
            const response = await getDocuments()
            setDocuments(response.data)
        } catch (error) {
            console.error('Error fetching documents:', error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchDocuments()
    }, [])

    const handleUpload = async (file: File) => {
        setLoading(true)
        try {
            await uploadDocument(file)
            await fetchDocuments()
        } catch (error) {
            console.error('Error uploading document:', error)
        } finally {
            setLoading(false)
        }
    }
    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault()
        if (loading) return
        setIsDragging(true)
    }

    const handleDragLeave = () => {
        setIsDragging(false)
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault()
        if (loading) return
        setIsDragging(false)
        const file = e.dataTransfer.files[0]
        if (file) {
            handleUpload(file)
        }
    }

    const handleDelete = async (id: number) => {
        if (!window.confirm('Are you sure you want to delete this document?')) return
        setLoading(true)
        try {
            await deleteDocument(id)
            await fetchDocuments()
        } catch (error) {
            console.error('Error deleting document:', error)
        } finally {
            setLoading(false)
        }
    }


    return (
        <div className="bg-creamBg min-h-screen font-body flex flex-col">
            <div className="max-w-5xl mx-auto px-6 py-8 flex-1 w-full">
                <header className="flex items-center mb-3">
                    <Link to="/documents" className="flex items-center mb-3">
                        <img src={duck} alt="Duck" className="w-16 h-16" />
                        <span className="text-2xl font-title text-black">Assistant</span>
                        <span className="text-2xl font-title text-violetText">-Duck</span>
                    </Link>
                </header>

                <h1>
                    <span className="text-5xl font-title">Welcome back! </span>
                    <span className="text-5xl font-title italic text-violetText">What are we reading today?</span>
                </h1>
                <p className="text-lg my-4 text-gray-500">Upload a PDF or open a recent one, and chat with it: ask questions, request summaries, and jump to the exact page of each answer.</p>

                <label
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`block border-2 border-dashed rounded-2xl bg-white flex flex-col items-center justify-center p-12 cursor-pointer text-center transition-colors my-6 ${loading ? 'opacity-50 cursor-not-allowed' : isDragging ? 'border-violetText bg-violet-50' : 'border-gray-300'
                        }`}
                >
                    <input
                        type="file"
                        disabled={loading}
                        className="hidden"
                        onChange={(e) => {
                            const file = e.target.files?.[0]
                            if (file) handleUpload(file)
                        }}
                    />
                    <div className="text-4xl mb-3">⬆</div>
                    <p className="text-lg font-semibold text-gray-700">
                        {loading ? 'Uploading...' : 'Drag a PDF here or click to upload'}
                    </p>
                    <p className="text-sm text-gray-400 mt-1">Up to 50 MB · only processed for your conversation</p>
                </label>

                <h2 className="text-2xl font-title mb-4">Recent Documents</h2>

                <ul className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {documents.map(doc => (
                        <li key={doc.id}>
                            <DocumentCard
                                doc={doc}
                                onDelete={() => handleDelete(doc.id)}
                                onClick={() => navigate(`/documents/${doc.id}`)}
                            />
                        </li>
                    ))}
                </ul>
            </div>
            <Footer />
        </div>
    )
}

export default DocumentsPage