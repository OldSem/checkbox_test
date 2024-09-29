from typing import Dict
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.models import User
from config.database import get_db


SECRET_KEY: str = "your_secret_key"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to create a JWT access token with an expiration time.
# The token is encoded using the provided data and includes an expiration timestamp.
# It is encoded with a secret key and an algorithm (HS256 in this case).
def create_access_token(data: Dict[str, str]) -> str:
    """
    Generates a JSON Web Token (JWT) with a specified expiration time.

    Parameters:
    - data: A dictionary containing the data to encode in the token.
      The dictionary is typically used to store user identification information.

    Returns:
    - A string representing the encoded JWT, which can be used for authenticating requests.

    The token includes an "exp" field that specifies the expiration time of the token.
    The expiration time is set based on the ACCESS_TOKEN_EXPIRE_MINUTES variable.
    """
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: Dict[str, str] = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_user_role(user: str = Depends(get_current_user)):
    return user.role


def admin_required(role: str = Depends(get_current_user_role)):
    if role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",

        )