from pydantic import BaseModel

class ProductIngredientCreate(BaseModel):
    ingredient_id: int
    quantity_required: float

class ProductIngredientOut(ProductIngredientCreate):
    class Config:
        orm_mode = True
