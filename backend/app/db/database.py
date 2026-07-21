from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind =engine)


print(engine)
print(type(engine))