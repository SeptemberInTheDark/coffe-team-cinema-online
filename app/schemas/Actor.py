from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, field_serializer
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class ActorCreateSchema(BaseModel):
    first_name: str
    last_name: str | None
    eng_full_name: str | None
    biography: str | None
    avatar: str | None
    height: int | None
    date_of_birth: date | None
    place_of_birth: str | None

    class Config:
        from_attributes = True


class ActorResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    eng_full_name: Optional[str] = None
    biography: Optional[str] = None
    avatar: Optional[str] = None
    height: Optional[int] = None
    date_of_birth: Optional[date] = None
    place_of_birth: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("date_of_birth", "created_at", "updated_at")
    def serialize_dates(self, value: date | datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True


class ActorUpdateSchema(ActorCreateSchema):
    first_name: str | None
    last_name: str | None
