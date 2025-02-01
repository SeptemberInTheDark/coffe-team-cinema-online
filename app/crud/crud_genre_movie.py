from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import movie


class GenreMovieCRUD:

    @staticmethod
    async def get_genre_id(session: AsyncSession, movie_id: int):
        query = select(movie.GenreMovie).where(movie.GenreMovie.movie_id == movie_id)
        result = await session.scalar(query)
        return result