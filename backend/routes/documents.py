from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal
from services import extract_text_from_pdf, chunk_text, get_embeddings
from models import Document, Chunk
from schemas import UploadResponse, DocumentResponse

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/upload/")
async def create_upload_file(
    file: UploadFile,
    db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.")
    try:
        text = extract_text_from_pdf(file.file)
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The PDF contains no readable text.")
        chunks = chunk_text(text, chunk_size=500, overlap=100)
        embeddings = get_embeddings(chunks)
        doc = Document(
        name=file.filename,
        size=file.size
        )
        db.add(doc)
        db.flush()  
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_db = Chunk(
                document_id=doc.id,
                text=chunk,
                embedding=embedding,
                chunk_index=i
            )
            db.add(chunk_db)

        db.commit()
        db.refresh(doc)

        return UploadResponse(
                document_id=doc.id,
                filename=doc.name,
                size=doc.size,
                chunks_count=len(chunks),
                message="File processed successfully"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@router.get("/", response_model=list[DocumentResponse])
async def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [DocumentResponse(
        id=doc.id,
        filename=doc.name,
        size=doc.size,
        created_at=doc.created_at
    ) for doc in documents]

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse(
        id=doc.id,
        filename=doc.name,
        size=doc.size,
        created_at=doc.created_at
    )

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}