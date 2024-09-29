import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Query, APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.orm import Session

from receipt import models, schemas
from auth import auth
from auth.models import User
from tools.output import render

from config.database import get_db
from tools.email import send_mock_email

router = APIRouter()


@router.get("/products/", response_model=List[schemas.ProductResponse])
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@router.post("/products/",
             response_model=schemas.ProductResponse,
             dependencies=[Depends(auth.admin_required)],
             status_code=status.HTTP_201_CREATED)
def create_products(products: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**products.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/receipts/", response_model=List[schemas.ReceiptResponseList])
async def get_receipts(offset: int = 0, limit: int = 10, db: Session = Depends(get_db),
                       current_user: User = Depends(auth.get_current_user),
                       created_from: Optional[datetime.datetime] = Query(None),
                       created_to: Optional[datetime.datetime] = Query(None),
                       min_total: Optional[float] = Query(None),
                       max_total: Optional[float] = Query(None),
                       payment_type: Optional[str] = Query(None),
                       last: Optional[str] = Query(None),
                       ):
    query = db.query(models.Receipt)
    if last:
        query = query.filter(models.Receipt.created_at >= (datetime.datetime.now() - relativedelta(**{f'{last}s': 1})))
    if created_from:
        query = query.filter(models.Receipt.created_at >= created_from)
    if created_to:
        query = query.filter(models.Receipt.created_at <= created_to)

    # total filter
    if min_total is not None:
        query = query.filter(models.Receipt.total >= min_total)
    if max_total is not None:
        query = query.filter(models.Receipt.total <= max_total)

    if payment_type:
        query = query.filter(models.Receipt.type == payment_type)
    receipts = query.filter(current_user == models.Receipt.owner).offset(offset).limit(limit).all()

    return receipts


@router.get("/receipts/{receipt_id}/show/",
            response_class=HTMLResponse
            )
async def get_receipts(receipt_id: int,
                       db: Session = Depends(get_db),
                       length: int = 25,
                       # current_user: User = Depends(auth.get_current_user),
                       ):
    query = db.query(models.Receipt)
    receipt = query.filter(models.Receipt.id == receipt_id).first()
    context = dict(company='ФОП Джонсонюк Борис',
                   receipt=receipt,
                   max_length=length)

    return render('receipt/templates/receipt.html', context)


@router.post("/receipts/",
             response_model=schemas.ReceiptResponse,
             dependencies=[Depends(auth.admin_required)],
             status_code=status.HTTP_201_CREATED)
def create_receipts(order: schemas.OrderCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(auth.get_current_user)):
    receipt = models.Receipt(type=order.payment.type, amount=order.payment.amount, owner=current_user)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    # add products
    receipt.total = 0
    for product in order.products:
        new_product = db.query(models.Product).filter(models.Product.name == product.name).first()
        if not new_product:
            new_product = models.Product(name=product.name, price=product.price)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)

        total = product.price * product.quantity
        product_receipt = models.ProductReceipt(
            product=new_product,
            receipt=receipt,
            price=product.price,
            quantity=product.quantity,
            total=total
        )
        receipt.total += total
        db.add(product_receipt)

    receipt.rest = receipt.amount - receipt.total
    db.commit()

    response_products = [
        schemas.ProductReceiptResponse(
            name=pr.product.name,
            price=pr.price,
            quantity=pr.quantity,
            total=pr.total
        )
        for pr in receipt.products
    ]

    response = schemas.ReceiptResponse(
        id=receipt.id,
        payment=schemas.ReceiptBase(type=receipt.type, amount=receipt.amount),

        total=receipt.total,
        rest=receipt.amount - receipt.total,
        products=response_products,
        created_at=receipt.created_at
    )
    return response
