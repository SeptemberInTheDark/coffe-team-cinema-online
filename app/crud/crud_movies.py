from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from typing import Optional

from sqlalchemy.orm import joinedload

from app.models.movie import GenreMovie, Genre
from app.schemas.Movie import MoveCreateSchema
from app.utils.logging import AppLogger
from app.models import movie

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
    async def create_movies(
            session: AsyncSession, movie_data: MoveCreateSchema
    ) -> Optional[movie.Movie]:
        try:
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
                operator=movie_data.operator or [],
                composer=movie_data.composer or [],
                actors=movie_data.actors or [],
                editor=movie_data.editor or [],
            )

            session.add(new_movie)
            await session.flush()  # Получаем ID фильма без коммита

            # Добавляем жанры
            if movie_data.genres:
                for genre_id in movie_data.genres:
                    # Проверяем существование жанра
                    genre = await session.get(Genre, genre_id)
                    if not genre:
                        await session.rollback()
                        logger.error(f"Жанр с ID {genre_id} не найден")
                        return None

                    # Создаем связь в genre_movie
                    genre_movie = GenreMovie(
                        genre_id=genre_id,
                        movie_id=new_movie.id
                    )
                    session.add(genre_movie)

            await session.commit()
            await session.refresh(new_movie)
            return new_movie

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании фильма: %s", str(e))
            return None


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
    async def update_movie(
            session: AsyncSession,
            movie_id: int,
            movie_data: MoveCreateSchema
    ):
        try:

            existing_movie = await session.get(movie.Movie, movie_id)
            if not existing_movie:
                return None

            update_data = movie_data.model_dump(exclude_unset=True)

            # Обновляем базовые поля
            for field, value in update_data.items():
                if field != "genres":  # Жанры обрабатываем отдельно
                    setattr(existing_movie, field, value)

            # Обрабатываем жанры, если они переданы
            if "genres" in update_data:
                # Удаляем старые связи
                await session.execute(
                    delete(GenreMovie).where(GenreMovie.movie_id == movie_id)
                )

                # Добавляем новые жанры
                genres = update_data["genres"]
                if genres:
                    # Проверяем существование жанров
                    existing_genres = await session.execute(
                        select(Genre.id).where(Genre.id.in_(genres))
                    )
                    existing_genres = existing_genres.scalars().all()

                    # Если есть несуществующие ID
                    if len(existing_genres) != len(genres):
                        invalid_ids = set(genres) - set(existing_genres)
                        logger.error(f"Несуществующие ID жанров: {invalid_ids}")
                        await session.rollback()
                        return None

                    # Добавляем новые связи
                    session.add_all([
                        GenreMovie(movie_id=movie_id, genre_id=genre_id)
                        for genre_id in genres
                    ])

            await session.commit()
            await session.refresh(existing_movie)
            return existing_movie

        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении фильма: {str(e)}")
            return None


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
    async def search_movies_by_genre(
            session: AsyncSession,
            genre_name: str,
            skip: int = 0,
            limit: int = 20
    ):
        query = (
            select(movie.Movie)
            .join(GenreMovie, GenreMovie.movie_id == movie.Movie.id)
            .join(Genre, Genre.id == GenreMovie.genre_id)
            .where(Genre.name == genre_name)
            .options(joinedload(movie.Movie.genres_link))
            .offset(skip)
            .limit(limit)
        )

        result = await session.scalars(query)
        return result.unique().all()
