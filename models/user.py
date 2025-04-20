from sqlalchemy import Column, Integer, String, Boolean, Enum
from database import Base
from sqlalchemy.orm import relationship

import enum

class RoleEnum(str, enum.Enum):
    owner = "owner"
    manager = "manager"
    costumer = "costumer"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    contact = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)
    role = Column(
        Enum(
            RoleEnum,
            name="roleenum",
            native_enum=True
        ),
        nullable=True
    )