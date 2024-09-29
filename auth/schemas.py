from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum


class UserBase(BaseModel):
    username: str
    role: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class OAuth2PasswordRequestJSON(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

