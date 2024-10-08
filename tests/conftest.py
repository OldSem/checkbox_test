import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.models import User
from receipt.models import Receipt, ProductReceipt, Product

# Тестовий engine
TEST_DATABASE_URL = os.environ.get('LOCAL_DB')
engine = create_engine(TEST_DATABASE_URL)

# Тестова сесія
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    """
    Фікстура для створення чистої тестової БД перед кожним тестом.
    """
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()
