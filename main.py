from typing import Union

from fastapi import FastAPI
from routers.stores import router as store_router
from routers.ingredients import router as ingredient_router
from routers.stock import router as stock_router
from routers.orders import router as orders_router
from routers.users import public_router, protect_router

app = FastAPI(title="API da Pizzaria", version="1.0.0")
app.include_router(store_router)
app.include_router(ingredient_router)
app.include_router(stock_router)
app.include_router(orders_router)
app.include_router(public_router)
app.include_router(protect_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}