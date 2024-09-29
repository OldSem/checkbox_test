import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as PyEnum


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


check_type_map = {
    'card': 'Картка',
    'cash': 'Готівка'
}


class CheckType(PyEnum):
    cash = "cash"
    card = "card"


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(CheckType), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2))
    rest = Column(DECIMAL(10, 2))
    user = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # relations
    owner = relationship("User", backref="Receipts")
    products = relationship("ProductReceipt", back_populates="receipt")

    @property
    def payment_type(self):
        translations = {
            CheckType.cash: "Готівка",
            CheckType.card: "Картка"
        }
        return translations.get(self.type, self.type)


class ProductReceipt(Base):
    __tablename__ = 'product_receipts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)

    receipt_id = Column(Integer, ForeignKey('receipts.id'), nullable=False)

    # relations
    product = relationship("Product")
    receipt = relationship("Receipt", back_populates="products")

