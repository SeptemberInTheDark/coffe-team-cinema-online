from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.movies.movie_handlers.movie_schemas import MoveCreateSchema
from src.utils.logging import AppLogger
from src.movies import models

logger = AppLogger().get_logger()


class MovesCRUD:

    @staticmethod
    async def get_move(session: AsyncSession, **kwargs) -> Optional[models.Movie]:
        return await session.scalar(select(models.Movie).filter_by(**kwargs))

    @staticmethod
    async def get_all_moves(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(models.Movie).offset(skip).limit(limit))
        return result.all()


    @staticmethod
    async def create_moves(session: AsyncSession, movie: MoveCreateSchema) -> Optional[models.Movie | bool]:
        add_movie = models.Movie(
            title=movie.title,
            description=movie.description,
            photo=movie.photo,
            release_year=movie.release_year,
            genre_id=movie.genre_id,
            duration=movie.duration,
            actors=movie.actors,
            director=movie.director
        )

        try:
            session.add(add_movie)
            await session.commit()
            await session.refresh(add_movie)
            return add_movie

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании пользователя: %s", e)
            return False

    @staticmethod
    async def delete_move(session: AsyncSession, **kwargs) -> bool:
        delete_movie = await session.get(models.Movie, **kwargs)
        if delete_movie:
            await session.delete(delete_movie)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_move(session: AsyncSession, **kwargs) -> Optional[models.Movie | bool]:
        update_movie = await session.get(models.Movie, **kwargs)
        if update_movie:
            update_movie.title = kwargs['title']
            update_movie.description = kwargs['description']
            update_movie.photo = kwargs['photo']
            update_movie.release_year = kwargs['release_year']
            update_movie.genre_id = kwargs['genre_id']
            update_movie.duration = kwargs['duration']
            update_movie.actors = kwargs['actors']
            update_movie.director = kwargs['director']
            await session.commit()
            await session.refresh(update_movie)
            return update_movie
        else:
            return False