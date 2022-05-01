# import uuid

from os import name
from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import JSON
from models.models import Base, User
from typing import List , Optional
# from uuid import UUID
from pydantic import BaseModel
import datetime
from fastapi import FastAPI, File, UploadFile


class RegisterUser(BaseModel):
    fname: str
    lname: str
    is_admin: bool
    username: str
    password : str
    email: str

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):

    New_password: str
    confirm_password: str

    class Config:
        orm_mode = True



class Address(BaseModel):

    name: str
    address_label: str
    address: str
    phone_no: str
    pincode: str
    latitude: float
    longtitude: float

class Cordinates(BaseModel):

    latitude: float
    longtitude: float
    distance: float

class Cal_two_cordinates(BaseModel):

    latitude1: float
    longtitude1: float
    latitude2: float
    longtitude2: float