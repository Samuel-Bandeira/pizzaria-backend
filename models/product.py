from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    store = relationship("Store", back_populates="products")
    ingredients = relationship("ProductIngredient", back_populates="product")
    orders = relationship("OrderItem", back_populates="product")