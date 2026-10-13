from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .models.user import User
from .models.document import Document
from app.db.database import engine,Base,get_db
from app.routes.users import router as user_router
from app.routes.auth import router as auth_router
from app.routes.documents import router as doc_router
from .models.document_text import DocumentText
from app.routes.ai import router as ai_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(doc_router)
app.include_router(ai_router)
Base.metadata.create_all(bind=engine)

app.add_middleware(CORSMiddleware,allow_origins=[ "http://localhost:5173",
        "http://127.0.0.1:5173",],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/")
def home():
    return {"DATABASEURL" : settings.DATABASE_URL,
            "DEBUG": settings.DEBUG}

