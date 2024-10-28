from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
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
    async def create_movies(session: AsyncSession, movie_data: MoveCreateSchema) -> Optional[models.Movie | bool]:
        # Создаем объект модели SQLAlchemy на основе Pydantic-схемы
        new_movie = models.Movie(
            title=movie_data.title,
            url_movie=movie_data.url_movie,
            description=movie_data.description,
            photo=movie_data.photo,
            release_year=movie_data.release_year,
            director=movie_data.director,
            actors=list(movie_data.actors),
            duration=movie_data.duration,
            genre_name=movie_data.genre_name,
        )
        try:
            session.add(new_movie)
            await session.commit()
            await session.refresh(new_movie)
            return new_movie

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании фильма: %s", e)
            return False

    @staticmethod
    async def delete_movie(session: AsyncSession, **kwargs) -> bool:
        movie = await session.scalar(select(models.Movie).filter_by(**kwargs))
        if movie:
            await session.delete(movie)
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


    @staticmethod
    async def search_movies(session: AsyncSession, query: str, skip: int = 0, limit: int = 20):
        """
        Поиск фильмов по любому слову из title и description.
        """
        search_query = f"%{query}%"
        result = await session.scalars(
            select(models.Movie)
            .where(or_(
                models.Movie.title.ilike(search_query),
                models.Movie.description.ilike(search_query)
            ))
            .offset(skip)
            .limit(limit)
        )
        return result.all()


    @staticmethod
    async def search_movies_by_genre(session: AsyncSession, genre_name: str, skip: int = 0, limit: int = 20):
        """
        Поиск фильмов по названию жанра.
        """
        result = await session.scalars(
            select(models.Movie).where(models.Movie.genre_name == genre_name)
            .offset(skip)
            .limit(limit)
        )
        return result.all()
