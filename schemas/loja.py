from pydantic import BaseModel

class LojaBase(BaseModel):
    name: str
    contact: str | None = None
    email: str | None = None
    is_active: bool = False
    latitude: float = 0.0
    longitude: float = 0.0

class LojaCreate(LojaBase):
    pass

class LojaUpdate(LojaBase):
    pass

class LojaOut(LojaBase):
    id: int
    
    class Config:
        orm_mode = True
