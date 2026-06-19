from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime,timezone

class Document(Base):
    __tablename__="documents"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="document", cascade="all, delete-orphan")