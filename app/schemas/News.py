from datetime import date, datetime

from pydantic import BaseModel, field_serializer

from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class NewsBaseSchema(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: date | datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True


class NewsCreateSchema(BaseModel):
    title: str
    sub_title: str | None
    text_news: str | None
    comment: int | None
    source: str | None

    class Config:
        from_attributes = True


class NewsResponseSchema(NewsBaseSchema):
    sub_title: str | None
    text_news: str | None
    comment: int | None
    source: str | None


class NewsMainListResponseSchema(NewsBaseSchema):
    sub_title: str | None
    text_news: str | None


class NewsListResponseSchema(NewsBaseSchema):
    comment: int | None
