from sqlmodel import Field, Relationship, SQLModel
from typing import List
from datetime import date


from backend.app.core.init_db import BaseModel
from .actor import Actor, ActorMovie
from .reward import RewardMovie
from .user import User


class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)

    movies: List["Movie"] = Relationship(back_populates="genres", link_model="GenreMovie")


class GenreMovie(SQLModel, table=True):
    __tablename__ = "genre_movie"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    genre_id: int = Field(foreign_key="public.genre.id", nullable=False)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)


class Trailer(SQLModel, table=True):
    __tablename__ = "trailer"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    name: str = Field(nullable=False)
    url_trailer: str = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="trailers")


class Category(SQLModel, table=True):
    __tablename__ = "category"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)

    movies: List["Movie"] = Relationship(back_populates="category")


class Poster(SQLModel, table=True):
    __tablename__ = "poster"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    photo: str = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="posters")


class Photo(SQLModel, table=True):
    __tablename__ = "photo"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    photo: str = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="photos")


class MovieComments(SQLModel, table=True):
    __tablename__ = "movie_comments"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    text: str = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")


class MovieRating(SQLModel, table=True):
    __tablename__ = "movie_rating"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="public.user.id", nullable=False)
    movie_id: int = Field(foreign_key="public.movie.id", nullable=False)
    rating: str = Field(nullable=False)

    movie: "Movie" = Relationship(back_populates="ratings")
    user: "User" = Relationship(back_populates="ratings")


class Movie(SQLModel, table=True):
    __tablename__ = "movie"
    __table_args__ = {"schema": "public"}

    id: int = Field(primary_key=True, index=True)
    url: str = Field(nullable=False)
    title: str = Field(nullable=False)
    eng_title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    avatar: str = Field(nullable=False)
    release_year: date = Field(nullable=False)
    director: str = Field(nullable=False)
    country: str = Field(nullable=False)
    part: int = Field(nullable=False)
    age_restriction: int = Field(nullable=False)
    duration: int = Field(nullable=False)
    category_id: int = Field(foreign_key="public.category.id", nullable=False)
    producer: str = Field(nullable=False)
    screenwriter: str = Field(nullable=False)
    operator: str = Field(nullable=False)
    composer: str = Field(nullable=False)
    artist: str = Field(nullable=False)
    editor: str = Field(nullable=False)

    actors: List[Actor] = Relationship(back_populates="movies", link_model=ActorMovie)
    category: "Category" = Relationship(back_populates="movies")
    ratings: List["MovieRating"] = Relationship(back_populates="movie")
    trailers: List["Trailer"] = Relationship(back_populates="movie")
    posters: List["Poster"] = Relationship(back_populates="movie")
    photos: List["Photo"] = Relationship(back_populates="movie")
    comments: List["MovieComments"] = Relationship(back_populates="movie")
    genres: List["Genre"] = Relationship(back_populates="movies", link_model="GenreMovie")
    rewards: List["RewardMovie"] = Relationship(back_populates="movie")
