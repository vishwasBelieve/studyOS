from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException,Cookie
from jose import jwt, JWTError
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Count not validate credentials")


def get_current_user(access_token:str | None = Cookie(default=None),db:Session= Depends(get_db)):

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    
    payload = verify_access_token(access_token)
    user_id = int(payload.get("sub"))
    stmt = select(User).where(User.id == user_id)
    current_user = db.execute(stmt).scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Credentials")
    return current_user
