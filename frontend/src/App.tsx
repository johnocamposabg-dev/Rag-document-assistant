import { BrowserRouter, Routes, Route } from 'react-router-dom'
import DocumentsPage from './pages/DocumentsPage'
import ChatPage from './pages/ChatPage'
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/documents/:id" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App 