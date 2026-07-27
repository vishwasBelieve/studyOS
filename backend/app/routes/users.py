from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserReponse,UserUpadte
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
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not founds")
    return user

@router.put("/{user_id}",response_model=UserReponse)
def update_user(user_id:int,user_update:UserUpadte,db:Session=Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")
    update_data = user_update.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(user,key,value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    stmt = select(User).where(User.id==user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/",response_model=list[UserReponse])
def get_users(db:Session = Depends(get_db),limit:int = 10,offset:int = 0):
    return db.execute(select(User).offset(offset).limit(limit)).scalars().all()

