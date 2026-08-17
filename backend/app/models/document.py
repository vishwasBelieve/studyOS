from uuid import uuid4
from sqlalchemy import String, Integer, BigInteger,DateTime, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


from app.db.database import Base

class Document(Base):

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key = True,default=uuid4)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    name:Mapped[str] = mapped_column(String(255),nullable=False)
    stored_name: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    file_path:Mapped[str] = mapped_column(String(500),nullable=False)
    mime_type:Mapped[str] = mapped_column(String(100),nullable=False)
    size:Mapped[int] = mapped_column(BigInteger,nullable=False)
    page_count:Mapped[int] = mapped_column(Integer,nullable=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updatedf_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    owner = relationship("User",back_populates="documents")
    texts = relationship("DocumentText",back_populates="document",cascade="all, delete-orphan")


    