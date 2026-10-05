from sqlalchemy.orm import mapped_column,Mapped,relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer,ForeignKey,Text,Boolean
from pgvector.sqlalchemy import Vector,vector
from sqlalchemy import UniqueConstraint

from app.db.database import Base

class DocumentText(Base):
    __tablename__ = "document_texts"
    id:Mapped[UUID] =  mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    document_id:Mapped[str] = mapped_column(ForeignKey("documents.id"),nullable=False)
    page_number:Mapped[int] = mapped_column(Integer,nullable=False)
    text:Mapped[str] = mapped_column(Text,nullable=False)
    paragraph_number:Mapped[int] = mapped_column(Integer)
    embedding: Mapped[Vector |None] = mapped_column(Vector(384),nullable=True)
    searchable:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    document = relationship("Document",back_populates="texts")





