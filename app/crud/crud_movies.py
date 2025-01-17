from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from typing import Optional

from app.schemas.Movie import MoveCreateSchema
from app.utils.logging import AppLogger
from app.models import movie, actor

logger = AppLogger().get_logger()


class MovesCRUD:

    @staticmethod
    async def get_movie(session: AsyncSession, **kwargs) -> Optional[movie.Movie]:
        return await session.scalar(select(movie.Movie).filter_by(**kwargs))

    @staticmethod
    async def get_movies_filter(session: AsyncSession, skip: int = 0, limit: int = 20, **kwargs, ):
        result = await session.scalars(select(movie.Movie).filter_by(**kwargs).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def get_all_movies(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(movie.Movie).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_movies(session: AsyncSession, movie_data: MoveCreateSchema) -> Optional[movie.Movie | bool]:
        new_movie = movie.Movie(
            title=movie_data.title,
            eng_title=movie_data.eng_title,
            url=movie_data.url,
            description=movie_data.description,
            avatar=movie_data.avatar,
            release_year=movie_data.release_year,
            director=movie_data.director,
            country=movie_data.country,
            part=movie_data.part,
            age_restriction=movie_data.age_restriction,
            duration=movie_data.duration,
            category_id=movie_data.category_id,
            producer=movie_data.producer,
            screenwriter=movie_data.screenwriter,
            operator=movie_data.operator,
            composer=movie_data.composer,
            artist=movie_data.artist,
            editor=movie_data.editor,
        )

        # Получение или создание актеров
        # for actor_name in movie_data.artist:
        #     actor_old = await session.scalar(select(actor.Actor).filter_by(first_name=actor_name))
        #     if actor_old is None:
        #         actor_new = actor.Actor(actor_name=actor_name)  # Создание нового актера
        #         session.add(actor_new)
        #
        #     new_movie.artist = actor_new  # Добавление актера к фильму

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
        film = await session.scalar(select(movie.Movie).filter_by(**kwargs))
        if film:
            await session.delete(film)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_movie(session: AsyncSession, movie_id: int, movie_data: MoveCreateSchema) -> Optional[
        movie.Movie | bool]:
        # Получение фильма по ID
        update_movie = await session.get(movie.Movie, movie_id)

        if update_movie:
            # Обновление полей фильма
            update_movie.title = movie_data.title
            update_movie.eng_title = movie_data.eng_title
            update_movie.url = movie_data.url
            update_movie.description = movie_data.description
            update_movie.avatar = movie_data.avatar
            update_movie.release_year = movie_data.release_year
            update_movie.director = movie_data.director
            update_movie.country = movie_data.country
            update_movie.part = movie_data.part
            update_movie.age_restriction = movie_data.age_restriction
            update_movie.duration = movie_data.duration
            update_movie.category_id = movie_data.category_id
            update_movie.producer = movie_data.producer
            update_movie.screenwriter = movie_data.screenwriter
            update_movie.operator = movie_data.operator
            update_movie.composer = movie_data.composer
            update_movie.artist = movie_data.artist
            update_movie.editor = movie_data.editor

            # Обновление актеров (если требуется)
            # if hasattr(movie_data, 'actors'):
            #     update_movie.artist.clear()
            #     for actor_name in movie_data.actors:
            #         actor_new = await session.scalar(select(actor.Actor).filter_by(name=actor_name))
            #         if actor_new is None:
            #             actor_new = actor.Actor(name=actor_name)
            #             session.add(actor)
            #         update_movie.actors.append(actor)

            await session.commit()
            await session.refresh(update_movie)
            return update_movie

        return False


    @staticmethod
    async def search_movies(session: AsyncSession, query: str, skip: int = 0, limit: int = 20):
        """
        Поиск фильмов по любому слову из title и description.
        """
        search_query = f"%{query}%"
        result = await session.scalars(
            select(movie.Movie)
            .where(or_(
                movie.Movie.title.ilike(search_query),
                movie.Movie.description.ilike(search_query)
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
        # TODO Переделать поиск по category_id
        result = await session.scalars(
            select(movie.Movie).where(movie.Movie.category_id == genre_name)
            .offset(skip)
            .limit(limit)
        )
        return result.all()
