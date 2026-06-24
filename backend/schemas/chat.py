from pydantic import BaseModel, Field

class Source(BaseModel):
    id: int = Field(..., description="chunk identifier")
    text: str = Field(..., description="the chunk text used as context")

class ChatRequest(BaseModel):
    document_id: int = Field(..., description="the unique identifier of the document to query")
    question: str = Field(..., description="the question to ask about the document")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="the answer to the question based on the document content")
    sources: list[Source] = Field(..., description="the chunks used to generate the answer")
