from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProductIngredient(Base):
    __tablename__ = "products_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_required = Column(Float, nullable=False)

    product = relationship("Product", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="products")
