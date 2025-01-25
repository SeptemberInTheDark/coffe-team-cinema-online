from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class MoveCreateSchema(BaseModel):
    title: str
    eng_title: str | None
    url: str | None
    description: str | None
    avatar: str | None
    release_year: date | None
    director: str | None
    country: str | None
    part: int | None
    age_restriction: int | None
    duration: int | None
    category_id: Optional[int] = None
    producer: List[str] | None
    screenwriter: List[str] | None
    operator: List[str] | None
    composer: List[str] | None
    actors: List[str] | None
    editor: List[str] | None
    genres: List[int] | None
    class Config:
        from_attributes = True


class MovieResponseSchema(BaseModel):
    id: int
    title: str
    eng_title: str | None
    url: str | None
    description: str | None
    avatar: str | None
    release_year: date | None
    director: str | None
    country: str | None
    part: int | None
    age_restriction: int | None
    duration: int | None
    category_id: int | None
    producer: List[str] | None
    screenwriter: List[str] | None
    operator: List[str] | None
    composer: List[str] | None
    actors: List[str] | None
    editor: List[str] | None
    genres: List[int] | None
    created_at: datetime
    updated_at: datetime

    @field_serializer("release_year", "created_at", "updated_at")
    def serialize_dates(self, value: date | datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True

class GenreCreateSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class MovieUpdateSchema(MoveCreateSchema):
    title: str | None
    genres: List[int]| None

