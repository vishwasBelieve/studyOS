from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserReponse
from sqlalchemy import select

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

@router.get("/{user_id}",response_model=UserReponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    stmt = select(User).where(User.id== user_id)
    user = db.execute(stmt).scalar_one()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not founds")
    return user