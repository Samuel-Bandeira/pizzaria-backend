from typing import Union

from fastapi import FastAPI
from routers.stores import router as store_router
from routers.ingredients import router as ingredient_router
from routers.stock import router as stock_router
from routers.orders import router as orders_router
from routers.users import public_router, protect_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API da Pizzaria", version="1.0.0")

origins = [
    "http://localhost:3000",  # frontend em desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] para permitir todas (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],     # permite todos os métodos: GET, POST, etc.
    allow_headers=["*"],     # permite todos os headers
)

app.include_router(store_router)
app.include_router(ingredient_router)
app.include_router(stock_router)
app.include_router(orders_router)
app.include_router(public_router)
app.include_router(protect_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}