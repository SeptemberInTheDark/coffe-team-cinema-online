from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from backend.app.models.movie import MovieRating, MovieComments
from backend.app.models.news import NewsViews, NewsComments

from backend.app.core.init_db import BaseModel


class Like(SQLModel, table=True):
    __tablename__ = "like"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    movie_id: int = Field(foreign_key=("public.movie.id"), nullable=False)
    like: bool = Field(default=False, nullable=False)

    user: "User" = Relationship(back_populates="likes")


class Favorite(SQLModel, table=True):
    __tablename__ = "favorite"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    movie_id = Field(foreign_key="public.movie.id", nullable=False)
    heart: bool = Field(default=True, nullable=False)

    user: "User" = Relationship(back_populates="favorites")


class Role(SQLModel, table=True):
    __tablename__ = "role"
    __table_args__ = {"schema": "public"}


    id: int = Field(primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    permissions: Optional[dict] = Field(sa_column_kwargs={"nullable": True}) # JSON ????

    users: List["User"] = Relationship(back_populates="role")

class SocialNetworks(SQLModel, table=True):
    __tablename__ = "social_networks"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    name: str = Field(max_length=50, nullable=False)
    url: str = Field(nullable=False)

    user: "User" = Relationship(back_populates="social_networks")

class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    avatar: str | None = Field(max_length=255, nullable=True)
    username: str = Field(max_length=255, nullable=False)
    first_name: str | None = Field(max_length=255, nullable=True)
    last_name: str| None = Field(max_length=255, nullable=True)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    phone: str = Field(max_length=255, nullable=False, unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    role_id: int = Field(foreign_key="public.user.id", nullable=False)
    country: str | None = Field(max_length=255, nullable=True)
    gender: str | None = Field(max_length=1, nullable=True)

    role: Role = Relationship(back_populates="users")
    social_networks: List[SocialNetworks] = Relationship(back_populates="user")
    likes: List[Like] = Relationship(back_populates="user")
    favorites: List[Favorite] = Relationship(back_populates="user")
    comments: List["MovieComments"] = Relationship(back_populates="user")
    ratings: List["MovieRating"] = Relationship(back_populates="user")
    news_views: List["NewsViews"] = Relationship(back_populates="user")
    news_comments: List["NewsComments"] = Relationship(back_populates="user")
