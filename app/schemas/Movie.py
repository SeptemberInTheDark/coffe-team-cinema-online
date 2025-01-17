from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.utils.logging import AppLogger

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
    eng_title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None
    release_year: Optional[date] = None
    director: Optional[str] = None
    country: Optional[str] = None
    part: Optional[int] = None
    age_restriction: Optional[int] = None
    duration: Optional[int] = None
    category_id: Optional[int] = None
    producer: Optional[str] = None
    screenwriter: Optional[str] = None
    operator: Optional[str] = None
    composer: Optional[str] = None
    actors: Optional[List[str]] = None
    editor: Optional[str] = None
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

