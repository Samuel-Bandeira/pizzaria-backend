from pydantic import BaseModel
from typing import Optional

class IngredientBase(BaseModel):
    name: str
    unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None

class IngredientOut(IngredientBase):
    id: int
    class Config:
        orm_mode = True
