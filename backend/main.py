from database import Base, engine
from models import Chat, Chunk, Document
from fastapi import FastAPI

app= FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}