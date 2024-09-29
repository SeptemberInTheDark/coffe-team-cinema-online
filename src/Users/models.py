from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey

from db import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    permissions = Column(JSON)


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), nullable=False)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    email = Column(String(length=255), nullable=False, unique=True, index=True)
    phone = Column(String(length=15), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False, default=2)
