import { BrowserRouter, Routes, Route, Navigate  } from 'react-router-dom'
import DocumentsPage from './pages/DocumentsPage'
import ChatPage from './pages/ChatPage'
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/documents" replace />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/documents/:id" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App 