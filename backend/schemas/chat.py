from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    document_id: int = Field(..., description="the unique identifier of the document to query")
    question: str = Field(..., description="the question to ask about the document")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="the answer to the question based on the document content")
    sources: list[int] = Field(..., description="the source of the answer, e.g., 'document' or 'knowledge_base'")