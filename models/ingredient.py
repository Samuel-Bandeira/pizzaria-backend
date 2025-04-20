from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=False)

    products = relationship("ProductIngredient", back_populates="ingredient")
    stock = relationship("Stock", back_populates="ingredients")
