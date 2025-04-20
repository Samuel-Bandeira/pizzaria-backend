from pydantic import BaseModel

class StockBase(BaseModel):
    store_id: int
    ingredient_id: int
    total_quantity: float
    used_quantity: float

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class StockOut(StockBase):
    id: int

    class Config:
        orm_mode = True