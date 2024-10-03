from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Text

from db import BaseModel
from src.Users.models import User


class Genre(BaseModel):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Movie(BaseModel):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    photo = Column(String(255), nullable=False)
    release_year = Column(Integer, nullable=False)
    director = Column(String(255), nullable=False)
    actors = Column(JSON, nullable=False)
    duration = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)


class Review(BaseModel):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    review_text = Column(Text, nullable=False)


class Rating(BaseModel):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    rating = Column(Integer, nullable=False)


class Actor(BaseModel):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    movie_id = Column(JSON, nullable=False)
    description = Column(Text, nullable=False)
    photo = Column(String(255), nullable=False)

