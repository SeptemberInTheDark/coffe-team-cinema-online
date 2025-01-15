from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.dialects.postgresql import VARCHAR

from app.core.init_db import BaseModel
from .movie import Movie


class ActorMovie(BaseModel):
    __tablename__ = "actor_movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("public.actor.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)


class Actor(BaseModel):
    __tablename__ = "actor"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    eng_full_name = Column(VARCHAR, nullable=False)
    biography = Column(Text, nullable=False)
    avatar = Column(VARCHAR, nullable=False)
    height = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    place_of_birth = Column(VARCHAR, nullable=False)





