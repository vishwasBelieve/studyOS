from fastapi import FastAPI
from .core.config import settings
from .models.user import User
from app.db.database import engine,Base,get_db
from app.routes.users import router as user_router
app = FastAPI()
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"DATABASEURL" : settings.DATABASE_URL,
            "DEBUG": settings.DEBUG}

