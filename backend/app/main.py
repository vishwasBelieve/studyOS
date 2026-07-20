from fastapi import FastAPI
from .core.config import settings

app = FastAPI()

@app.get("/")
def home():
    return {"DATABASEURL" : settings.DATABASE_URL,
            "DEBUG": settings.DEBUG}
