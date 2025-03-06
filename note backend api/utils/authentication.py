
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from models.user import  UserModel
from models.database import session_maker
from schemas.user import UserSignUpSchema, UserLoginSchema, Token

from environs import env
env.read_env()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")
db = session_maker()

def verify_password(plain_password, hashed_password) ->bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def get_user_auth(user_email: str) -> UserSignUpSchema|None:
    user_found = db.scalars(select(UserModel).where(UserModel.email == user_email)).first()
    if user_found and user_found.is_deleted == False: # exclude deactivated account.
        user = UserSignUpSchema(**user_found.__dict__)
        return user
    return None


def authenticate_user(user: UserLoginSchema) -> UserSignUpSchema:
    user_found = get_user_auth(user.email)
    if not user_found:
        return False
    if not verify_password(user.password, user_found.password):
        return False
    return user_found

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=env('SECRET_KEY'), algorithm = env('ALGORITHM'))
    return encoded_jwt

def generate_login_token(user_email:str):
    access_token_expires = timedelta(minutes= int(env('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(data={"sub": user_email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env('SECRET_KEY'), algorithms=[env('ALGORITHM')])
        print(payload)
        user_email = payload.get("sub")
        
        if user_email is None:
            raise credentials_exception
        token_data = user_email 
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_auth( user_email=user_email)
    print(user.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[UserSignUpSchema, Depends(get_current_user)],):
    if current_user.email:
        raise HTTPException(status_code=400, detail="Inactive user.")
    return current_user



