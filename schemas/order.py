from pydantic import BaseModel, conlist
from typing import Optional, List, Annotated
from models.order import OrderStatus
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    store_id: int
    items: List[OrderItemCreate]

class OrderUpdate(OrderCreate):
    pass

class OrderPatch(BaseModel):
    status: Optional[OrderStatus]

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    store_id: int
    total_value: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
