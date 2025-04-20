from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    contact: str
    email: str
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str
