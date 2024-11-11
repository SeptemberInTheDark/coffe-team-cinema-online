from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from db import BaseModel
from src.Users.models import User

actor_movies = Table(
    'actor_movies', BaseModel.metadata,
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)

class Genre(BaseModel):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)


class Movie(BaseModel):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    url_movie = Column(Text)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    photo = Column(String(255), nullable=False)
    release_year = Column(Integer, nullable=False)
    director = Column(String(255), nullable=False)
    actors = relationship('Actor', secondary=actor_movies, back_populates='movies')
    duration = Column(Integer, nullable=False)
    genre_name = Column(String, ForeignKey(Genre.name), nullable=False)



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
    movies = relationship('Movie', secondary=actor_movies, back_populates='actors')
    description = Column(Text)
    photo = Column(String(255))

