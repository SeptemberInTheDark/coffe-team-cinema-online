from app.schemas.News import NewsResponseSchema
from app.models import news

from typing import Optional, List

from fastapi import Form


def form_news_data(movies: list | Optional[news.News]) -> list[dict]:
    news_data = []
    processed_ids = set()

    for obj in movies:
        if obj.id in processed_ids:
            continue
        news_dict = {
            "id": obj.id,
            "title": obj.title,
            "sub_title": obj.sub_title,
            "text_news": obj.text_news,
            "comment": obj.comment,
            "source": obj.source,
            "created_at": obj.created_at,  # Оставляем как datetime
            "updated_at": obj.updated_at,  # Оставляем как datetime
        }
        news_data.append(NewsResponseSchema(**news_dict).model_dump())
        processed_ids.add(obj.id)

    return news_data


async def parse_form_data(
        title: str = Form(...),
        sub_title: Optional[str] = Form(None),
        text_news: Optional[str] = Form(None),
        comment: Optional[int] = Form(None),
        source: Optional[str] = Form(None),
):
    # TODO эту функцию (to_list) нужно вынести в отдельный файл и импортировать при необходимости, чтобы соблюдать DRY
    def to_list(value: Optional[str]) -> Optional[List[str]]:
        if value:
            return [item.strip() for item in value.split(',') if item.strip()]
        return None

    return {
        "title": title,
        "sub_title": sub_title,
        "text_news": text_news,
        "comment": comment,
        "source": source,
    }
