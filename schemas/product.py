from pydantic import BaseModel, conlist
from typing import Optional, List, Annotated
from .products_ingredients import ProductIngredientCreate, ProductIngredientOut
from .ingredient import IngredientOut
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

class ProductCreate(ProductBase):
    ingredients:  Annotated[
        list[ProductIngredientCreate],
        conlist(ProductIngredientCreate, min_length=1)
    ]

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    ingredients: List[ProductIngredientOut] = []
    available: bool
    missing_ingredients: List[IngredientOut]

    class Config:
        orm_mode = True
