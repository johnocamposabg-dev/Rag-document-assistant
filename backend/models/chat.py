from database import Base
from sqlalchemy import  Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

class Chat(Base):
    __tablename__="chats"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    chunks_used: Mapped[str] = mapped_column(String, nullable=True)
    document: Mapped["Document"] = relationship("Document", back_populates="chats")
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
