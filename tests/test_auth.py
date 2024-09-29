import json

import pytest
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient
from httpx import Response

from main import app

from auth.models import User
from tools.db import reset_sequence

client = TestClient(app)


def user_create() -> Response:
    return client.post("/users/", json={
         "username": "testuser",
         "role": "Admin",
         "email": "testuser@gmail.com",
         "password": "testpassword"
    })


def user_delete(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    reset_sequence(user.__class__.__tablename__, db)


def test_users(db: Session) -> None:
    response = client.get("/users/")
    assert response.status_code == 200


def test_registration(db: Session):
    response = user_create()
    user_delete(db, int(response.json()["id"]))
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_login(db: Session):
    user_response = user_create()
    response = client.post("/token", json={
        "username": "testuser",
        "password": "testpassword"
    })
    user_delete(db, int(user_response.json()["id"]))
    assert response.status_code == 200
    assert "access_token" in response.json()
