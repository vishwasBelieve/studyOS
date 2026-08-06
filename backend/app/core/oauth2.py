from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from jose import jwt, JWTError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Count not validate credentials")


