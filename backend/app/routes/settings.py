from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserReponse,UserUpadte
from sqlalchemy import select
from app.core.security import verify_password,hash_password
from app.core.oauth2 import get_current_user
from pydantic import BaseModel
from typing import Literal

from app.db.database import get_db
from app.models.user import User


router = APIRouter(prefix="/settings",tags=["Settings"])  

class AIKeyRequest(BaseModel):
    provider : Literal["openai","anthropic","google"]
    api_key : str   

@router.put("/ai_keys")
def add_api_key(data:AIKeyRequest,db:Session = Depends(get_db),user = Depends(get_current_user)):
    if not data.api_key.strip():
        raise HTTPException(status_code=400,detail="API key is required")

    keys = dict(user.ai_keys or {})
    keys[data.provider] = data.api_key.strip()

    user.ai_keys = keys
    db.commit()

    return {"message" : "AI provider settings saved"}