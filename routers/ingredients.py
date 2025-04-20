from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.ingredient import Ingredient
from schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientOut
from typing import List
from utils.routers import ProtectedRouter

router = ProtectedRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("/", response_model=IngredientOut)
def create_ingredient(data: IngredientCreate, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter_by(name=data.name).first()
    if ingredient:
        raise HTTPException(status_code=409, detail=f"O ingrediente {data.name} já existe.")
    
    obj = Ingredient(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[IngredientOut])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()

@router.get("/{ingredient_id}", response_model=IngredientOut)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ingredient).get(ingredient_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")
    return obj

@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, data: IngredientCreate, db: Session = Depends(get_db)):
    obj = db.query(Ingredient).get(ingredient_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")
    
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{ingredient_id}", response_model=IngredientOut)
def patch_ingredient(ingredient_id: int, data: IngredientUpdate, db: Session = Depends(get_db)):
    obj = db.query(Ingredient).get(ingredient_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ingredient).get(ingredient_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")
    db.delete(obj)
    db.commit()
    return None
