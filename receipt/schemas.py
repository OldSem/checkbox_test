from pydantic import BaseModel, condecimal
from typing import List, Optional, Union
from enum import Enum
from datetime import datetime


class ReceiptType(str, Enum):
    cash = "cash"
    card = "card"


class ProductBase(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ReceiptBase(BaseModel):
    type: ReceiptType
    amount: condecimal(max_digits=10, decimal_places=2)


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptResponse(BaseModel):
    id: int
    products: Optional[List['ProductReceiptResponse']] = []
    payment: ReceiptBase
    total: condecimal(max_digits=10, decimal_places=2)
    rest: condecimal(max_digits=10, decimal_places=2)
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class ReceiptResponseList(ReceiptBase):
    id: int
    total: condecimal(max_digits=10, decimal_places=2)
    rest: Union[condecimal(max_digits=10, decimal_places=2), None]
    created_at: datetime


class ProductReceiptBase(BaseModel):
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: int
    amount: condecimal(max_digits=10, decimal_places=2)


class ProductReceiptCreate(BaseModel):
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    name: str
    quantity: int


class ProductReceiptResponse(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: condecimal(max_digits=10, decimal_places=2)
    total: condecimal(max_digits=10, decimal_places=2)


    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    products: List[ProductReceiptCreate]
    payment: ReceiptCreate
