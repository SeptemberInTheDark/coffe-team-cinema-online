from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.movies.models import Movie
from src.utils.logging import AppLogger

logger = AppLogger().get_logger()


class MovieSchema(BaseModel):
    id: int | None = None
    is_active: str
    title = str
    description: str
    photo: str
    release_year: int
    director: str
    actors: str
    duration: int
    genre_id: int
    is_active: Optional[bool] = True


class MoveCreateSchema(Movie):
    title: str
    description: str
    photo: str
    release_year: int
    director: str
    actors: str
    duration: int
    genre_id: int
    model_config = ConfigDict(from_attributes=True)
