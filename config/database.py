import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from base.models import Base


SQLALCHEMY_DATABASE_URL = os.environ.get('LOCAL_DB')
# SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@localhost/checkbox'
print(f'++++++++++++++++++{SQLALCHEMY_DATABASE_URL}++++++++++++++++++++++++++++++++++++++++')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
