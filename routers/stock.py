from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from models.stock import Stock
from schemas.stock import StockCreate, StockUpdate, StockOut
from models.ingredient import Ingredient
from utils.routers import ProtectedRouter

router = ProtectedRouter(prefix="/stock", tags=["Stock"])

@router.post("/", response_model=StockOut)
def create_stock(data: StockCreate, db: Session = Depends(get_db)):
    existing = db.query(Stock).filter_by(
        store_id=data.store_id,
        ingredient_id=data.ingredient_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Estoque já existe para esse ingrediente na loja.")
    
    ingredient = db.query(Ingredient).get(data.ingredient_id)

    if not ingredient:
        raise HTTPException(status_code=409, detail=f"O ingrediente de ID {data.ingredient_id} não existe.")

    obj = Stock(
        store_id=data.store_id,
        ingredient_id=data.ingredient_id,
        total_quantity= data.total_quantity,
        used_quantity= 0.0
    )
    
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[StockOut])
def list_stock(db: Session = Depends(get_db)):
    return db.query(Stock).all()

@router.get("/{stock_id}", response_model=StockOut)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    obj = db.query(Stock).get(stock_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estoque não encontrado.")
    return obj

@router.put("/{stock_id}", response_model=StockOut)
def update_stock(stock_id: int, data: StockCreate, db: Session = Depends(get_db)):
    obj = db.query(Stock).get(stock_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estoque não encontrado.")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{stock_id}", response_model=StockOut)
def patch_stock(stock_id: int, data: StockUpdate, db: Session = Depends(get_db)):
    obj = db.query(Stock).get(stock_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estoque não encontrado.")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{stock_id}", status_code=204)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    obj = db.query(Stock).get(stock_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estoque não encontrado.")
    db.delete(obj)
    db.commit()
    return None
