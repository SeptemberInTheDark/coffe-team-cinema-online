from datetime import datetime

from sqlalchemy import select, delete, extract, func, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from sqlalchemy.orm import joinedload, selectinload

from app.schemas.News import NewsCreateSchema, NewsResponseSchema
from app.utils.logging import AppLogger
from app.models.news import News

logger = AppLogger().get_logger()


class NewsCRUD:

    @staticmethod
    async def get_news(session: AsyncSession, **kwargs) -> Optional[News]:
        query = select(News).filter_by(**kwargs)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all_news_main_page(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(News).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_news(session: AsyncSession, news_data: NewsCreateSchema) -> Optional[News]:
        try:
            new_news = News(
                title=news_data.title,
                sub_title=news_data.sub_title,
                text_news=news_data.text_news,
                comment=news_data.comment,
                source=news_data.source,
            )

            session.add(new_news)
            await session.commit()
            await session.refresh(new_news)
            return new_news

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании новости: %s", str(e))
            return None

    @staticmethod
    async def delete_news(session: AsyncSession, **kwargs) -> bool:
        news = await session.scalar(select(News).filter_by(**kwargs))
        if news:
            await session.delete(news)
            await session.commit()
            return True
        else:
            return False
