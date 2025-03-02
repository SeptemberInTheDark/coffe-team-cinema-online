from app.schemas.News import NewsListResponseSchema, NewsMainListResponseSchema
from app.models import news

from typing import Optional, List

from fastapi import Form


def form_news_data_main_page(news_list: list | Optional[news.News]) -> list[dict]:
    news_data = []
    processed_ids = set()

    for obj in news_list:
        if obj.id in processed_ids:
            continue
        news_dict = NewsMainListResponseSchema.from_orm(obj).model_dump()
        news_data.append(news_dict)
        processed_ids.add(obj.id)

    return news_data


# Повтор кода временный т.к. в будущем эти две функции могут измениться
def form_news_data_news_page(news_list: list | Optional[news.News]) -> list[dict]:
    news_data = []
    processed_ids = set()

    for obj in news_list:
        if obj.id in processed_ids:
            continue
        news_dict = NewsListResponseSchema.from_orm(obj).model_dump()
        news_data.append(news_dict)
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
