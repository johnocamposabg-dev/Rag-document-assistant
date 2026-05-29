from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

class Document(Base):
    __tablename__="documents"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="document")
    chunks: Mapped[list["Chunk"]] = relationship("Chunk", back_populates="document")