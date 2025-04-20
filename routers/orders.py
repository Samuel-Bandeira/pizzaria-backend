from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.order import Order
from models.order_item import OrderItem
from models.ingredient import Ingredient
from models.product import Product
from models.stock import Stock
from schemas.order import OrderCreate, OrderOut, OrderUpdate, OrderPatch
from dependencies import get_db
from utils.routers import ProtectedRouter

router = ProtectedRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    items = []
    total = 0.0

    for item in order_data.items:
        product = db.query(Product).get(item.product_id)

        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        
        for product_ingredient in product.ingredients:
            ingredient = db.query(Ingredient).get(product_ingredient.id)
            ingredient_stock = db.query(Stock).filter_by(store_id=order_data.store_id, ingredient_id=product_ingredient.id).first()

            if not ingredient_stock:
                raise HTTPException(status_code=409, detail=f"Não há estoque para o ingrediente {ingredient.name}. Por isso o pedido não pode ser efetuado.")
            
            used_quantity = product_ingredient.quantity_required * item.quantity

            if(used_quantity > ingredient_stock.total_quantity - ingredient_stock.used_quantity):
                raise HTTPException(status_code=409, detail=f"Não há estoque suficiente de {ingredient.name} para realizar a operação.")
            
            ingredient_stock.used_quantity += used_quantity
            
        subtotal = product.price * item.quantity
        total += subtotal
        items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.price))

    order = Order(store_id=order_data.store_id, total_value=total, items=items, status="RECEIVED")

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.patch("/{order_id}", response_model=OrderOut)
def patch_order(order_id: int, patch_data: OrderPatch, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    for campo, valor in patch_data.dict(exclude_unset=True).items():
        setattr(order, campo, valor)

    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(order)
    db.commit()
    return