from database import Base
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pgvector.sqlalchemy import Vector

class Chunk(Base):
    __tablename__="chunks"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str]= mapped_column(Text, nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=False)
    chunk_index: Mapped[int]= mapped_column(Integer, nullable=False)
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))