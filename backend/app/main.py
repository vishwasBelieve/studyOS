from fastapi import FastAPI
from .core.config import settings
from .models.user import User
from app.db.database import engine,Base
app = FastAPI()

@app.get("/")
def home():
    return {"DATABASEURL" : settings.DATABASE_URL,
            "DEBUG": settings.DEBUG}

Base.metadata.create_all(bind=engine)