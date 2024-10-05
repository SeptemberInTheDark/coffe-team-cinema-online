from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from src.utils.logging import AppLogger

logger = AppLogger().get_logger()


class MovieSchema(BaseModel):
    id: int | None = None
    is_active: str
    title: str
    description: str
    photo: str
    release_year: int
    director: str
    actors: str
    duration: int
    genre_id: int
    is_active: Optional[bool] = True


class MoveCreateSchema(BaseModel):
    title: str
    description: str
    photo: str
    release_year: int
    director: str
    actors: List[str]
    duration: int
    genre_id: int
    model_config = ConfigDict(from_attributes=True)


class GenreCreateSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

