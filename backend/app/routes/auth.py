from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.auth import Login
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.security import verify_password,hash_password
from sqlalchemy import select
from app.core.security import create_access_token

router = APIRouter(prefix="/login",tags=["Login"])

@router.post("/")
def login(user_credentials:Login,db:Session = Depends(get_db)):
    stmt = select(User).where(User.email == user_credentials.email)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Credentials")
    password_test = verify_password(user_credentials.password,user.hashed_password)
    if not password_test:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Incorrect Credentials")
    access_token = create_access_token({"sub":str(user.id)})
    return {"access_token" : access_token,
            "token_type" : "bearer"}