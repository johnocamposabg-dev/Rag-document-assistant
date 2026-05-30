from database import Base, engine
from models import Chat, Chunk, Document
from fastapi import FastAPI
from routes.documents import router as documents_router

app= FastAPI()
app.include_router(documents_router, prefix="/documents", tags=["documents"])
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}