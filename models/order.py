from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from database import Base

class OrderStatus(PyEnum):
    RECEIVED = "RECEIVED"
    IN_PROGRESS = "IN_PROGRESS"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    total_value = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.RECEIVED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    store = relationship("Store")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
