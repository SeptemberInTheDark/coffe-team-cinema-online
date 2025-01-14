from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.app.schemas.Movie import GenreCreateSchema
from backend.app.utils.logging import AppLogger
from backend.app.models import movie as models

logger = AppLogger().get_logger()


class ActorsCRUD:
    @staticmethod
    async def get_actor(session: AsyncSession, **kwargs) -> Optional[models.Genre]:
        return await session.scalar(select(models.Actor).filter_by(**kwargs))

    @staticmethod
    async def get_actors_filter(session: AsyncSession, skip: int = 0, limit: int = 20, **kwargs, ):
        result = await session.scalars(select(models.Actor).filter_by(**kwargs).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def get_all_actors(session: AsyncSession, skip: int = 0, limit: int = 10):
        result = await session.scalars(select(models.Actor).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_actor(session: AsyncSession, actor: GenreCreateSchema) -> Optional[models.Genre | bool]:
        add_genre = models.Genre(
            name=actor.name,
            description=actor.description,
            photo=actor.photo,
            movies=actor.movies
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
    async def delete_actor(session: AsyncSession, **kwargs) -> bool:
        delete_genre = await session.get(models.Genre, **kwargs)
        if delete_genre:
            await session.delete(delete_genre)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_actor(session: AsyncSession, **kwargs) -> Optional[models.Genre | bool]:
        update_genre = await session.get(models.Genre, **kwargs)
        if update_genre:
            update_genre.title = kwargs['name']
            await session.commit()
            await session.refresh(update_genre)
            return update_genre
        else:
            return False
