from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal
from services import extract_text_from_pdf, chunk_text, get_embeddings
from models import Document, Chunk
from schemas import UploadResponse, DocumentResponse
from pypdf import PdfReader

MAX_PAGES=50

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
def create_upload_file(
    file: UploadFile,
    db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.")
    reader = PdfReader(file.file)
    if len(reader.pages) > MAX_PAGES:
        raise HTTPException(
            status_code=400,
            detail= f"The PDF has more than {MAX_PAGES} pages")
    try:
        text = extract_text_from_pdf(reader)
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The PDF contains no readable text.")
        chunks = chunk_text(text, chunk_size=500, overlap=100)

        doc = Document(
            name=file.filename,
            size=file.size
        )
        db.add(doc)
        db.flush()

        batch_size = 100
        chunk_index = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_embeddings = get_embeddings(batch)
            for chunk, embedding in zip(batch, batch_embeddings):
                chunk_db = Chunk(
                    document_id=doc.id,
                    text=chunk,
                    embedding=embedding,
                    chunk_index=chunk_index
                )
                db.add(chunk_db)
                chunk_index += 1
            db.commit()

        db.refresh(doc)

        return UploadResponse(
                document_id=doc.id,
                filename=doc.name,
                size=doc.size,
                chunks_count=len(chunks),
                message="File processed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [DocumentResponse(
        id=doc.id,
        filename=doc.name,
        size=doc.size,
        created_at=doc.created_at
    ) for doc in documents]

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
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
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}