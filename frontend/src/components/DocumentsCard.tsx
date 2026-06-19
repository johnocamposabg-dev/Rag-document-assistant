import { formatFileSize, formatDate, getInitial } from '../utils/format'
import type { Document } from '../types'

interface DocumentCardProps {
    doc: Document
    onDelete: () => void
    onClick: () => void
}

function DocumentCard({ doc, onDelete, onClick }: DocumentCardProps) {
    return (
        <div
            onClick={onClick}
            className="bg-white rounded-xl border-l-4 border-violetText p-4 cursor-pointer hover:shadow-md transition-shadow"
        >
            <div className="flex justify-between items-start mb-3">
                <span className="text-4xl font-title text-gray-400">
                    {getInitial(doc.filename)}
                </span>
                <span className="text-xs bg-violetText/10 text-violetText px-2 py-1 rounded font-semibold">
                    PDF
                </span>
            </div>
            <p className="font-semibold text-gray-800 truncate">{doc.filename}</p>
            <p className="text-sm text-gray-400 mt-1">
                {formatFileSize(doc.size)} · {formatDate(doc.created_at)}
            </p>
            <button
                onClick={(e) => { e.stopPropagation(); onDelete() }}
                className="text-sm text-gray-400 hover:text-red-500 mt-3"
            >
                Delete
            </button>
        </div>
    )
}

export default DocumentCard