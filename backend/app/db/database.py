from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind =engine)

class Base(DeclarativeBase):
    pass
