from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.movies.movie_schemas import MoveCreateSchema
from src.utils.logging import AppLogger
from src.movies import models

logger = AppLogger().get_logger()


class MovesCRUD:

    @staticmethod
    async def get_movie(session: AsyncSession, **kwargs) -> Optional[models.Movie]:
        return await session.scalar(select(models.Movie).filter_by(**kwargs))

    @staticmethod
    async def get_movies_filter(session: AsyncSession, skip: int = 0, limit: int = 20, **kwargs, ):
        result = await session.scalars(select(models.Movie).filter_by(**kwargs).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def get_all_movies(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(models.Movie).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_movies(session: AsyncSession, movie: MoveCreateSchema) -> Optional[models.Movie | bool]:
        add_movie = models.Movie(
            title=movie.title,
            description=movie.description,
            photo=movie.photo,
            release_year=movie.release_year,
            genre_name=movie.genre_name,
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
            logger.error("Ошибка при создании фильма: %s", e)
            return False

    @staticmethod
    async def delete_movie(session: AsyncSession, **kwargs) -> bool:
        delete_movie = await session.get(models.Movie, **kwargs)
        if delete_movie:
            await session.delete(delete_movie)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_movie(session: AsyncSession, **kwargs) -> Optional[models.Movie | bool]:
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
