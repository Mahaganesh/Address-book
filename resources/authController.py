from logging import raiseExceptions
from fastapi.openapi.models import Schema
from datetime import datetime, timedelta
from typing import Optional

from jose.constants import Algorithms
from models.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from config.base_config import BaseConfig
from config.dev_config import Configuration
from models import models, get_db
from passlib.context import CryptContext

import os



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)
    return encoded_jwt

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email==token_data).first()

    if user is None:
        raise credentials_exception
    return user


@router.post('/authorize')
def authorize(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_name = form_data.username.lower()
    password = form_data.password
    print(user_name)
    print(password)
    db_user = db.query(models.User).filter(models.User.username == user_name).first()
    if db_user:
        if db_user.verify_password(password):
            access_token_expires = timedelta(minutes=BaseConfig.REFRESH_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data = {'sub': db_user.email}, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(data = {'sub': db_user.email}, expires_delta=access_token_expires)
            print(access_token)
            return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer', 'user_uid': db_user.uuid, 'username':user_name}  
        else:
            raise HTTPException(status_code=400, detail='Password Incorrect') 
    else:
        raise HTTPException(status_code=400, detail='Incorrect username')



@router.get("/users/me")
def get_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        user_uuid = current_user.uuid
        db_user = db.query(models.User).filter(models.User.uuid == user_uuid).first()
        del db_user.password
        return db_user

    else:
        HTTPException(status_code=400, detail="User Not Found")



@router.post("/forget_password")
def forget_password(reset_password: schemas.ResetPassword, email:str, db: Session = Depends(get_db)):
    email = email.lower()
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        if len(reset_password.New_password) < 8:
            raise HTTPException(status_code=400, detail="New Password is less than 8 character")
        elif len(reset_password.confirm_password) < 8:
            raise HTTPException(status_code=400, detail="Confirm Password is less than 8 character")

        if reset_password.New_password == reset_password.confirm_password:
            db_user.hash_password(reset_password.New_password)
            db.commit()
            raise HTTPException(status_code=200, detail="Password Updated Successfully")
        else:
            raise HTTPException(status_code=400, detail="Passwords dosen't match") 
    else:
        raise HTTPException(status_code=400, detail='User does not exist')