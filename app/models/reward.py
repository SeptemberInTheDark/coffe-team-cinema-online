from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from app.core.init_db import BaseModel


class RewardActor(BaseModel):
    __tablename__ = "reward_actor"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("public.actor.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("public.reward.id"), nullable=False)
    year = Column(Integer, nullable=False)


class RewardMovie(BaseModel):
    __tablename__ = "reward_movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("public.reward.id"), nullable=False)
    year = Column(Integer, nullable=False)


class Reward(BaseModel):
    __tablename__ = "reward"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, nullable=False)
    avatar = Column(VARCHAR, nullable=False)
    nomination = Column(VARCHAR, nullable=False)
