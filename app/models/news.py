from sqlmodel import Field, Relationship, SQLModel
from typing import List

from app.models.actor import Actor
from app.models.user import User


class NewsActor(SQLModel, table=True):
    __tablename__ = "news_actor"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    actor_id: int = Field(foreign_key="public.actor.id", nullable=False)
    news_id: int = Field(foreign_key="public.news.id", nullable=False)

    actor: "Actor" = Relationship(back_populates="news")
    news: "News" = Relationship(back_populates="actors")


class NewsViews(SQLModel, table=True):
    __tablename__ = "news_views"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    news_id: int = Field(foreign_key="public.news.id", nullable=False)
    is_vies: bool = Field(default=False)

    user: "User" = Relationship(back_populates="news_views")
    news: "News" = Relationship(back_populates="views")


class NewsComments(SQLModel, table=True):
    __tablename__ = "news_comments"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    news_id: int = Field(foreign_key="public.news.id", nullable=False)
    text_comment: bool = Field(default=False)

    user: "User" = Relationship(back_populates="news_comments")
    news: "News" = Relationship(back_populates="comments")


class News(SQLModel, table=True):
    __tablename__ = "news"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    title: str = Field(max_length=50, nullable=False)
    sub_title: str = Field(max_length=255, nullable=False)
    text_news: str = Field(nullable=False)
    source: str = Field(max_length=255, nullable=False)

    actors: List["NewsActor"] = Relationship(back_populates="news")
    views: List["NewsViews"] = Relationship(back_populates="news")
    comments: List["NewsComments"] = Relationship(back_populates="news")


