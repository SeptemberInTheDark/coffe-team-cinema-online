from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import AppLogger
from app.models import movie as models

logger = AppLogger().get_logger()


class CategoryCRUD:
    @staticmethod
    async def get_all_categories(session: AsyncSession, skip: int = 0, limit: int = 10):
        result = await session.scalars(select(models.Category).offset(skip).limit(limit))
        return result.all()