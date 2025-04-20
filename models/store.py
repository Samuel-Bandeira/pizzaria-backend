from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base
from sqlalchemy.orm import relationship
from .stock import Stock

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="store")
    products = relationship("Product", back_populates="store")