from pydantic import BaseModel, Field
from datetime import datetime

class UploadResponse(BaseModel):
    document_id: int = Field(..., description="use this document_id to query the document status and content")
    filename: str = Field(..., description="the original filename of the uploaded document")
    size: int = Field(..., description="the size of the uploaded document in bytes")
    chunks_count: int = Field(..., description="the number of chunks the document is split into for processing")
    message: str = Field(..., description="a message indicating the result of the upload operation")

class DocumentResponse(BaseModel):
    id: int= Field(..., description="the unique identifier for the document response")
    filename: str = Field(..., description="the original filename of the document")
    size: int = Field(..., description="the size of the document in bytes")
    created_at: datetime = Field(..., description="the timestamp when the document was created")