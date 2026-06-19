import { useNavigate, useParams, Link } from 'react-router-dom'
import { useState } from 'react'
import { queryChat } from '../services/api'
import ReactMarkdown from 'react-markdown'
import duck from '../assets/duck.png'
import Footer from '../components/Down'

interface Message {
    role: 'user' | 'assistant'
    content: string
}

function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([])
    const [question, setQuestion] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const { id } = useParams<{ id: string }>()

    const handleSubmit = async () => {
        if (!question.trim() || !id) return
        setMessages(prev => [...prev, { role: 'user', content: question }])
        setQuestion('')
        setLoading(true)
        try {
            const response = await queryChat(question, parseInt(id))
            setMessages(prev => [...prev, { role: 'assistant', content: response.data.answer }])
        } catch (error) {
            console.error('Error querying chat:', error)
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
                    <span className="text-4xl font-title">Ask me anything. </span>
                    <span className="text-4xl font-title italic text-violetText">I'll find the answer in your document.</span>
                </h1>

                <div className="my-8 bg-white rounded-2xl border border-gray-200 h-[60vh] flex flex-col">
                    <div className="flex-1 overflow-y-auto p-4">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex mb-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[70%] rounded-2xl px-4 py-2 ${msg.role === 'user' ? 'bg-violetText text-white' : 'bg-gray-100 text-gray-800'}`}>
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>

                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start mb-3">
                                <div className="bg-gray-100 rounded-5xl px-4 py-2">
                                    <span className="font-bold animate-bounce">.</span><span className="font-bold animate-bounce" style={{ animationDelay: '0.2s' }}>.</span><span className="font-bold animate-bounce" style={{ animationDelay: '0.4s' }}>.</span>
                                </div>
                            </div>
                        )
                        }
                    </div>
                    <div className="border-t border-gray-200 p-4 flex gap-2">
                        <input
                            type="text"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !loading && question.trim()) {
                                    handleSubmit()
                                }
                            }}
                            disabled={loading}
                            className="flex-1 rounded-full border border-gray-300 px-4 py-2 focus:outline-none focus:border-violetText"
                        />
                        <button
                            onClick={handleSubmit}
                            disabled={loading || !question.trim()}
                            className="bg-violetText text-white rounded-full px-5 py-2 disabled:opacity-50"
                        >
                            {loading ? 'Asking...' : 'Ask'}
                        </button>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    )
}
export default ChatPage