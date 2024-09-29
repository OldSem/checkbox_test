from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as PyEnum

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String)
    role = Column(String)


class Role(PyEnum):
    ADMIN = "Admin"
    USER = "User"
    MANAGER = "Manager"
