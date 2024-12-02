from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.dialects.postgresql import VARCHAR

from db import BaseModel
from models.user import User


class Genre(BaseModel):
    __tablename__ = "genre"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, nullable=False)


class GenreMovie(BaseModel):
    __tablename__ = "genre_movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey("public.genre.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)


class Trailer(BaseModel):
    __tablename__ = "trailer"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer,ForeignKey("public.movie.id"), nullable=False)
    name = Column(VARCHAR, nullable=False)
    url_trailer = Column(Text, nullable=False)


class Category(BaseModel):
    __tablename__ = "category"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, nullable=False)


class Poster(BaseModel):
    __tablename__ = "poster"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    photo = Column(VARCHAR, nullable=False)


class Photo(BaseModel):
    __tablename__ = "photo"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    photo = Column(VARCHAR, nullable=False)


class MovieComments(BaseModel):
    __tablename__ = "movie_comments"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    text = Column(Text, nullable=False)


class MovieRating(BaseModel):
    __tablename__ = "movie_rating"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    rating = Column(Integer, nullable=False)


class Movie(BaseModel):
    __tablename__ = "movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    title = Column(VARCHAR, nullable=False)
    eng_title = Column(VARCHAR, nullable=False)
    description = Column(Text, nullable=False)
    avatar = Column(VARCHAR, nullable=False)
    release_year = Column(Date, nullable=False)
    director = Column(VARCHAR, nullable=False)
    country = Column(VARCHAR, nullable=False)
    part = Column(Integer, nullable=False)
    age_restriction = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    category_id = Column(Integer,ForeignKey("public.category.id"), nullable=False)
    producer = Column(VARCHAR, nullable=False)
    screenwriter = Column(VARCHAR, nullable=False)
    operator = Column(VARCHAR, nullable=False)
    composer = Column(VARCHAR, nullable=False)
    artist = Column(VARCHAR, nullable=False)
    editor = Column(VARCHAR, nullable=False)



