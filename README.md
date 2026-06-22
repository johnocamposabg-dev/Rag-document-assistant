# 🦆 Assistant-Duck

> RAG assistant for analyzing and querying PDFs. Upload your PDF and ask whatever you need — the assistant answers with the most relevant information, strictly within the context of the document.

**🔗 [Live Demo](https://rag-document-assistant-mu.vercel.app)**

## Screenshots

![Documents page](frontend/public/Documents-Page.png)

![Chat in action](frontend/public/Chat-Page.png)

## Features

- 📄 Upload PDFs via drag & drop or file picker
- 💬 Chat with your documents in natural language
- 🔍 Semantic search powered by vector embeddings
- 🎯 Answers grounded strictly in document content
- 🗂️ Manage the shared document library: view and delete
- ⚡ Markdown-formatted responses with loading states

## Tech Stack

**Backend**
- FastAPI (Python)
- Uvicorn (ASGI server)
- PostgreSQL + pgvector (vector similarity search)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- pypdf (PDF text extraction)
- sentence-transformers (`all-MiniLM-L6-v2` for local embeddings)
- Anthropic Claude API (LLM)
- pytest (testing)

**Frontend**
- React 19 + TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- react-markdown (rendering formatted AI responses)

**Infrastructure & Deployment**
- Docker (local PostgreSQL with pgvector)
- Railway (backend + database)
- Vercel (frontend)

## How It Works

Assistant-Duck uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions based strictly on the content of your documents:

```mermaid
flowchart LR
    A[PDF Upload] --> B[Text Extraction]
    B --> C[Chunking]
    C --> D[Embeddings]
    D --> E[(pgvector DB)]
    F[User Question] --> G[Query Embedding]
    G --> E
    E --> H[Top 5 Chunks]
    H --> I[Claude API]
    I --> J[Answer]
```

1. **Upload & extract** — Text is extracted from the PDF using `pypdf`.
2. **Chunking** — The text is split into 500-character chunks with 100-character overlap to preserve context across boundaries (chunks under 50 chars are discarded).
3. **Embeddings** — Each chunk is converted into a 384-dimension vector using a local `sentence-transformers` model (`all-MiniLM-L6-v2`).
4. **Storage** — Chunks and embeddings are stored in PostgreSQL via the `pgvector` extension.
5. **Retrieval** — Your question is embedded the same way, and pgvector finds the 5 most similar chunks using cosine distance.
6. **Generation** — Those chunks are passed as context to Claude, which generates an answer grounded only in the retrieved content.

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- Docker (for local PostgreSQL with pgvector)
- An Anthropic API key

### Backend

```bash
# From the project root, start the database
docker compose up -d

# Set up the backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt

# Create a .env file (see Environment Variables below)

# Run the server
uvicorn main:app --reload
```

The API runs at `http://localhost:8000` (docs at `/docs`).

### Frontend

```bash
cd frontend
npm install

# Create a .env file with VITE_API_URL=http://localhost:8000

npm run dev
```

The app runs at `http://localhost:5173`.

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (e.g. `postgresql+psycopg://user:password@localhost:5432/dbname`) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL (e.g. `http://localhost:8000`) |

## Limitations & Roadmap

This is a portfolio project with some known limitations and planned improvements:

**Current limitations**
- **Single shared library** — There's no authentication; all users share the same document library.
- **Synchronous processing** — Document upload processes embeddings in-request, so large PDFs (hundreds of pages) can be slow or hit memory limits on the free-tier deployment (1 GB RAM).
- **Cold starts** — The free-tier backend may take a few seconds to wake up after inactivity.

**Roadmap**
- [ ] User authentication with per-user document libraries
- [ ] Background processing for uploads (non-blocking, with task queue)
- [ ] Batch embedding generation to handle large documents within memory limits
- [ ] Support additional document formats (.docx, .txt, .md) beyond PDF
- [ ] Display source references in chat responses (backend already returns them)
- [ ] Improved upload feedback (animated progress indicator)
- [ ] User-facing error messages instead of silent console errors
- [ ] Response streaming for faster perceived response time
- [ ] Frontend tests (Vitest + React Testing Library)

## Author

Built by John Ocampos — [LinkedIn](https://linkedin.com/in/john-ocampos) · [GitHub](https://github.com/johnocamposabg-dev)