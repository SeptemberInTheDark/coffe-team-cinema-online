from sqlmodel import Field, Relationship, SQLModel
from typing import List
from .movie import Movie
from datetime import date

from .news import NewsActor
from .reward import RewardActor


class ActorMovie(SQLModel, table=True):
    __tablename__ = "actor_movie"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    actor_id: int = Field(foreign_key="public.actor.id", nullable=False)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)


class Actor(SQLModel, table=True):
    __tablename__ = "actor"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    eng_full_name: str = Field(nullable=False)
    biography: str = Field(nullable=False)
    avatar: str = Field(nullable=False)
    height: str = Field(nullable=False)
    date_of_birth: date = Field(nullable=False)
    place_of_birth: str = Field(nullable=False)

    movies: List["Movie"] = Relationship(back_populates="actors", link_model=ActorMovie)
    rewards: List["RewardActor"] = Relationship(back_populates="actor")
    news: List["NewsActor"] = Relationship(back_populates="actor")




