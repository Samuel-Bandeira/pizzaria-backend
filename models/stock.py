from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    total_quantity = Column(Float, default=0.0)
    used_quantity = Column(Float, default=0.0)
    store = relationship("Store", back_populates="stock")
    ingredients = relationship("Ingredient", back_populates="stock")