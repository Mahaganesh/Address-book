from email.policy import default
from enum import unique
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, DateTime, Text, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from models import Base, engine
import bcrypt


Base = declarative_base(bind=engine)

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):

    __tablename__ = "users"

    uuid = Column(String,primary_key=True, default=generate_uuid, unique=True)
    username = Column(String(100), unique=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(200), unique=True)
    password = Column(LargeBinary)
    mobile_no = Column(String(20))
    is_deleted  = Column(Boolean, default=False)
    is_active = Column(Boolean)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(String, ForeignKey('users.uuid'))
    updated_by = Column(String, ForeignKey('users.uuid'))
    
    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password):
            return True
        else:
            return False

class Address(Base):

    __tablename__ = "Address"
    
    uuid = Column(String,primary_key=True, default=generate_uuid, unique=True)
    name = Column(String(200))
    address_label = Column(String(20))
    address = Column(String(300))
    phone_no = Column(String(25))
    pincode = Column(String(50))
    latitude = Column(String)
    longitude = Column(String)
    is_deleted  = Column(Boolean, default=False)
    is_active = Column(Boolean)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(String, ForeignKey('users.uuid'))
    updated_by = Column(String, ForeignKey('users.uuid'))