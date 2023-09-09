from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError  
import bcrypt
from config.database import engine, SessionLocal, Base
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from CRUD.crud import get_user
from schemas.schemas import *

SECRET_KEY = "secreto"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DB = SessionLocal()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:  # To create a acccess token is necesary set a 
    to_encode  = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    token_encode: str = jwt.encode(to_encode, key=SECRET_KEY, algorithm="HS256")
    return token_encode


def decode_token(token_encode: str) -> dict:
    user_info: dict = jwt.decode(token_encode, key=SECRET_KEY, algorithms=["HS256"])
    return user_info


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')



