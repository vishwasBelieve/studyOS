from sqlalchemy.orm import mapped_column,Mapped,relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer,ForeignKey,Text

from app.db.database import Base

class DocumentText(Base):
    __tablename__ = "document_texts"
    id:Mapped[UUID] =  mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    document_id:Mapped[str] = mapped_column(ForeignKey("documents.id"),nullable=False)
    page_number:Mapped[int] = mapped_column(Integer,nullable=False,unique=True)
    text:Mapped[str] = mapped_column(Text,nullable=False)

    document = relationship("Document",back_populates="texts")





