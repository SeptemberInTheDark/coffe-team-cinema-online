from sqlmodel import Field, Relationship, SQLModel

from app.models.actor import Actor
from app.models.movie import Movie
from typing import List


class RewardActor(SQLModel, table=True):
    __tablename__ = "reward_actor"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    actor_id: int = Field(foreign_key="public.actor.id", nullable=False)
    reward_id: int = Field(foreign_key="public.reward.id",nullable=False)
    year: int = Field(nullable=False)

    actor: "Actor" = Relationship(back_populates="rewards")
    reward: "Reward" = Relationship(back_populates="actors")


class RewardMovie(SQLModel, table=True):
    __tablename__ = "reward_movie"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    reward_id: int = Field(foreign_key="public.reward.id", nullable=False)
    year: int = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="rewards")
    reward: "Reward" = Relationship(back_populates="movies")


class Reward(SQLModel, table=True):
    __tablename__ = "reward"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    name: int = Field(nullable=False)
    avatar: int = Field(nullable=False)
    nomination: str = Field(nullable=False)

    actors: List["RewardActor"] = Relationship(back_populates="reward")
    movies: List["RewardMovie"] = Relationship(back_populates="reward")
