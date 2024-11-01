from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.movies.movie_schemas import GenreCreateSchema
from src.utils.logging import AppLogger
from src.movies import models

logger = AppLogger().get_logger()


class GenreCRUD:

    @staticmethod
    async def get_genre(session: AsyncSession, **kwargs) -> Optional[models.Genre]:
        return await session.scalar(select(models.Genre).filter_by(**kwargs))

    @staticmethod
    async def get_genres_filter(session: AsyncSession, skip: int = 0, limit: int = 20, **kwargs, ):
        result = await session.scalars(select(models.Genre).filter_by(**kwargs).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def get_all_genres(session: AsyncSession, skip: int = 0, limit: int = 10):
        result = await session.scalars(select(models.Genre).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_genre(session: AsyncSession, genre: GenreCreateSchema) -> Optional[models.Genre | bool]:
        add_genre = models.Genre(
            name=genre.name,
        )
        try:
            session.add(add_genre)
            await session.commit()
            await session.refresh(add_genre)
            return add_genre

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании жанра: %s", e)
            return False

    @staticmethod
    async def delete_genre(session: AsyncSession, **kwargs) -> bool:
        delete_genre = await session.get(models.Genre, **kwargs)
        if delete_genre:
            await session.delete(delete_genre)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_genre(session: AsyncSession, **kwargs) -> Optional[models.Genre | bool]:
        update_genre = await session.get(models.Genre, **kwargs)
        if update_genre:
            update_genre.title = kwargs['name']
            await session.commit()
            await session.refresh(update_genre)
            return update_genre
        else:
            return False
