import pytest
from sqlalchemy.orm.session import Session

from fastapi.testclient import TestClient
from tools.db import reset_sequence
from receipt.models import Receipt, ProductReceipt
from main import app
from tests.test_auth import user_create, user_delete


client = TestClient(app)


@pytest.fixture
def auth_token(db):
    user_response = user_create()
    response = client.post("/token", json={
        "username": "testuser",
        "password": "testpassword"
    })
    try:
        yield response.json()["access_token"]
    finally:
        user_delete(db, int(user_response.json()["id"]))


def receipt_delete(db: Session, instance_id: int):
    instance = db.query(Receipt).filter(Receipt.id == instance_id).first()
    for sub_instance in instance.products:
        db.delete(sub_instance)
    db.delete(instance)
    db.commit()
    reset_sequence(sub_instance.__class__.__tablename__, db)
    reset_sequence(instance.__class__.__tablename__, db)


def test_create_receipt(auth_token, db):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = client.post("/receipts/", json={
        "products": [
            {
                "name": "apple",
                "price": 10.5,
                "quantity": 2
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 21.0
        }
    }, headers=headers)
    receipt_delete(db, int(response.json()["id"]))
    assert response.status_code == 201
    assert response.json()["total"] == '21.00'


def test_get_receipts(auth_token, db):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = client.get("/receipts/", params={"offset": 0, "limit": 5}, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) <= 5


def test_get_receipt_public(db):
    receipt_id = 1  # Example id
    response = client.get(f"/receipts/{receipt_id}/show/")
    assert response.status_code == 200
    # assert "total" in response.json()


def test_invalid_create_receipt(auth_token, db):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = client.post("/receipts/", json={
        "products": [
            {
                "name": "apple",
                "price": -10.5,  # Неприпустима ціна
                "quantity": 2
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 21.0
        }
    }, headers=headers)
    assert response.status_code == 422