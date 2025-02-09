from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Text, Date, JSON
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.init_db import BaseModel



class Genre(BaseModel):
    __tablename__ = "genre"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, nullable=False)
    movies_link = relationship("GenreMovie", back_populates="genre")


class GenreMovie(BaseModel):
    __tablename__ = "genre_movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey("public.genre.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)

    genre = relationship("Genre", back_populates="movies_link")
    movie = relationship("Movie", back_populates="genres_link")


class Trailer(BaseModel):
    __tablename__ = "trailer"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    name = Column(VARCHAR, nullable=True)
    url_trailer = Column(Text, nullable=True)


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
    photo = Column(VARCHAR, nullable=True)


class Photo(BaseModel):
    __tablename__ = "photo"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    photo = Column(VARCHAR, nullable=True)


class MovieComments(BaseModel):
    __tablename__ = "movie_comments"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    text = Column(Text, nullable=True)


class MovieRating(BaseModel):
    __tablename__ = "movie_rating"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("public.movie.id"), nullable=False)
    rating = Column(Integer, nullable=True)


class Movie(BaseModel):
    __tablename__ = "movie"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=True)
    title = Column(VARCHAR, nullable=False)
    eng_title = Column(VARCHAR, nullable=True)
    description = Column(Text, nullable=True)
    avatar = Column(VARCHAR, nullable=True)
    release_year = Column(Date, nullable=True)
    director = Column(VARCHAR, nullable=True)
    country = Column(VARCHAR, nullable=True)
    part = Column(Integer, nullable=True)
    age_restriction = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("public.category.id"), nullable=True)
    producer: Mapped[List[str]] = mapped_column(JSON)
    screenwriter: Mapped[List[str]] = mapped_column(JSON)
    operator: Mapped[List[str]] = mapped_column(JSON)
    composer: Mapped[List[str]] = mapped_column(JSON)
    actors: Mapped[List[str]] = mapped_column(JSON)
    editor: Mapped[List[str]] = mapped_column(JSON)
    genres_link = relationship("GenreMovie", back_populates="movie")
