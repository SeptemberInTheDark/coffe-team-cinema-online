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
    eng_title: str
    url: str
    description: str
    avatar: str
    release_year: date
    director: str
    country: str
    part: int
    age_restriction: int
    duration: int
    category_id: int
    producer: str
    screenwriter: str
    operator: str
    composer: str
    actors: str
    editor: str
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

