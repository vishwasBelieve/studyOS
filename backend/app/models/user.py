from app.db.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB


class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    hashed_password : Mapped[str] = mapped_column(String(255),nullable=False)
    email : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    is_active: Mapped[bool] = mapped_column(default=True,nullable=False)
    ai_keys: Mapped[dict] = mapped_column(JSONB,default=dict,nullable=False)

    documents = relationship("Document",back_populates="owner",cascade="all,delete-orphan")
