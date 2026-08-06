from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings

password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password:str) -> str:
    return password_hash.hash(password)

def verify_password(password,hashed_password:str)->bool:
    return password_hash.verify(password,hashed_password)

def create_access_token(data:dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire

    encoded_jwt = jwt.encode(payload = to_encode,algorithm=ALGORITHM,key=settings.SECRET_KEY)

    return encoded_jwt