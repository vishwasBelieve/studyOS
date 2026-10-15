from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserReponse(BaseModel):
    id : int
    email : str

class UserUpadte(BaseModel):
    username : str | None = None
    email : str |None = None
