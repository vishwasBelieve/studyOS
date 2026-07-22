from app.db.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String
class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(30),nullable=False,unique=True,index =True)
    hashed_password : Mapped[str] = mapped_column(String(255),nullable=False)
    email : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    is_active: Mapped[bool] = mapped_column(default=True,nullable=False)
