from pydantic import BaseModel, ConfigDict
from typing import List
from models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    contact: str
    email: str
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
    
class UserLogin(BaseModel):
    email: str
    password: str
