from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate

from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/")
def create_user(user_data:UserCreate,db:Session = Depends(get_db)):
    user = User(username = user_data.username,email=user_data.email,hashed_password=user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user