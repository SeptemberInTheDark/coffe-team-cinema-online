from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, field_serializer
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class NewsCreateSchema(BaseModel):
    title: str
    sub_title: str | None
    text_news: str | None
    comment: int | None
    source: str | None

    class Config:
        from_attributes = True


class NewsResponseSchema(BaseModel):
    id: int
    title: str
    sub_title: str | None
    text_news: str | None
    comment: int | None
    source: str | None
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: date | datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True
