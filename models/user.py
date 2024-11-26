from sqlalchemy import Column, Integer, Boolean, JSON, ForeignKey, CHAR, Text
from sqlalchemy.dialects.postgresql import VARCHAR

from db import BaseModel
from models.movie import Movie


class Like(BaseModel):
    __tablename__ = "like"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    like = Column(Boolean, default=False, nullable=False)


class Favorite(BaseModel):
    __tablename__ = "favorite"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=True)
    heart = Column(Boolean, default=False)


class Role(BaseModel):
    __tablename__ = "role"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(length=50), nullable=False)
    permissions = Column(JSON, nullable=True)


class SocialNetworks(BaseModel):
    __tablename__ = "social_networks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    name = Column(VARCHAR(length=50), nullable=True)
    url = Column(Text, nullable=True)


class User(BaseModel):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    avatar = Column(VARCHAR(length=255), nullable=True)
    username = Column(VARCHAR(length=255), nullable=False)
    first_name = Column(VARCHAR(length=255), nullable=True)
    last_name = Column(VARCHAR(length=255), nullable=True)
    email = Column(VARCHAR(length=255), nullable=False, unique=True, index=True)
    phone = Column(VARCHAR(length=20), nullable=False, unique=True, index=True)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("public.role.id"), nullable=True)
    country = Column(VARCHAR(length=255), nullable=True)
    gender = Column(CHAR(length=1), nullable=True)

