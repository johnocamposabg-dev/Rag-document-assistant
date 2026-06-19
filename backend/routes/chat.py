from services import get_embeddings, get_answer
from schemas import ChatRequest, ChatResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Document, Chat, Chunk

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/query/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == request.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    embeddings = get_embeddings([request.question])
    query_vector = embeddings[0]
    chunks = db.query(Chunk).filter(Chunk.document_id == request.document_id).all()
    if not chunks:
        raise HTTPException(status_code=404, detail="No chunks found for this document")
    results = db.query(Chunk).filter(Chunk.document_id == request.document_id).order_by(Chunk.embedding.cosine_distance(query_vector)).limit(5).all()
    context = "\n\n".join([c.text for c in results])
    return ChatResponse(answer=get_answer(request.question, context), sources=[c.id for c in results])