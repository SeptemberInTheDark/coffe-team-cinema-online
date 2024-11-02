from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
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
    url_movie: str
    description: str
    photo: str
    release_year: int
    director: str
    actors: List[str]
    duration: int
    genre_name: str
    class Config:
        from_attributes = True


class GenreCreateSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class ActorCreateSchema(BaseModel):
    name: str = Field(..., max_length=255, description="Имя актера")
    description: str = Field(..., description="Описание актера")
    photo: str = Field(..., description="Ссылка на фото актера")
    movies: List[str] = Field(..., description="Список фильмов, в которых снимался актер")

