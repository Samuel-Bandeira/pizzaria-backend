from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.store import Store
from models.ingredient import Ingredient
from models.products_ingredients import ProductIngredient
from models.product import Product
from schemas.loja import LojaCreate, LojaUpdate, LojaOut
from schemas.product import ProductOut, ProductCreate
from dependencies import get_db
from utils.routers import ProtectedRouter

router = ProtectedRouter(prefix="/stores", tags=["Stores"])

@router.post("/", response_model=LojaOut)
def create_store(loja: LojaCreate, db: Session = Depends(get_db)):
    nova = Store(**loja.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/{loja_id}", response_model=LojaOut)
def get_store_by_id(loja_id: int, db: Session = Depends(get_db)):
    loja = db.query(Store).get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return loja

@router.get("/{store_id}/products", response_model=list[ProductOut])
def get_store_by_id(store_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.store_id == store_id)

@router.post("/{store_id}/products", response_model=ProductOut)
def create_product_in_store(store_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    exists = db.query(Product).filter_by(name=product.name).first()

    if exists:
        raise HTTPException(
            status_code= 500,
            detail=f"O Produto {product.name} já existe."
        )
    
    store = db.query(Store).get(store_id)

    if not store: 
        raise HTTPException(
            status_code= 500,
            detail=f"A store de ID {store_id} não foi encontrada."
        )

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        is_active=product.is_active,
        store_id=store_id
    )
    db.add(db_product)
    db.flush()

    for item in product.ingredients:
        ingredient = db.query(Ingredient).get(item.ingredient_id)
        if not ingredient:
            raise HTTPException(
                status_code=400,
                detail=f"Ingrediente com ID {item.ingredient_id} não existe."
            )
        
        assoc = ProductIngredient(
            product_id=db_product.id,
            ingredient_id=item.ingredient_id,
            quantity_required=item.quantity_required
        )
        db.add(assoc)

    db.commit()
    db.refresh(db_product)

    return db_product

@router.get("/", response_model=list[LojaOut])
def get_store(db: Session = Depends(get_db)):
    return db.query(Store).all()

@router.put("/{loja_id}", response_model=LojaOut)
def put_store(loja_id: int, loja_data: LojaUpdate, db: Session = Depends(get_db)):
    loja = db.query(Store).get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")

    dados = loja_data.dict()
    for campo, valor in dados.items():
        setattr(loja, campo, valor)

    db.commit()
    db.refresh(loja)
    return loja

@router.patch("/{loja_id}", response_model=LojaOut)
def patch_store(loja_id: int, loja_data: LojaUpdate, db: Session = Depends(get_db)):
    loja = db.query(Store).get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")

    dados = loja_data.dict(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(loja, campo, valor)

    db.commit()
    db.refresh(loja)
    return loja

@router.delete("/{loja_id}")
def delete_store(loja_id: int, db: Session = Depends(get_db)):
    loja = db.query(Store).get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    db.delete(loja)
    db.commit()
    return {"mensagem": "Loja excluída com sucesso"}
