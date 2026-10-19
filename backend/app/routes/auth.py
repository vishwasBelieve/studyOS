from fastapi import APIRouter,Depends,HTTPException,status,Response
from app.schemas.auth import Login
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.security import verify_password,hash_password
from sqlalchemy import select
from app.core.security import create_access_token
from app.core.oauth2 import oauth2_scheme,verify_access_token,get_current_user
from fastapi import Response
from app.schemas.user import UserReponse
router = APIRouter(prefix="/login",tags=["Login"])

@router.post("/")
def login(user_credentials:Login,response:Response,db:Session = Depends(get_db)):
    stmt = select(User).where(User.email == user_credentials.email)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Credentials")
    password_test = verify_password(user_credentials.password,user.hashed_password)
    if not password_test:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Incorrect Credentials")
    access_token = create_access_token({"sub":str(user.id)})
    response.set_cookie(
        key="access_token",
        value = access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age =3600,
        path="/",
    )
    print(access_token)
    return {"message":"Login Sucessful"}


@router.get("/me",response_model=UserReponse)
def get_me(current_user = Depends(get_current_user),):
    return {
        "id":current_user.id,
        "email":current_user.email

    }

@router.post("/logout")
def logout(response:Response):
    response.delete_cookie(key = "access_token",path="/",httponly=True,samesite="lax",)
    return {"message":"Logged out successfully"}