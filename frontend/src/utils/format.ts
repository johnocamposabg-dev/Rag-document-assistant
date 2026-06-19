export function formatFileSize(size: number): string {
    if (size < 1024) {
        return `${size} B`
    } else if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(1)} KB`
    } else{
        return `${(size / (1024 * 1024)).toFixed(2)} MB`
}}

export function getInitial(filename: string): string {
    return filename.charAt(0).toUpperCase()
}

export function formatDate(isoString: string): string {
    const date = new Date(isoString)
    return date.toLocaleDateString(undefined, {month: 'short', day: 'numeric' })
}