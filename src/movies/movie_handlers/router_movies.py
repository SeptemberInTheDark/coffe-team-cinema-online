from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.movies.movie_handlers.crud_moves import MovesCRUD
from src.movies.movie_schemas import MoveCreateSchema
from fastapi.responses import JSONResponse


from src.utils.logging import AppLogger

logger = AppLogger().get_logger()

moves_router = APIRouter(
    prefix='/api',
    tags=['Movies'],
)


@moves_router.post(
    path="add_movie",
    summary="Добавить фильм",
    response_description="Добавленный фильм"
)
async def add_movie(
        session: AsyncSession = Depends(get_db),
        title: str = Form(...),
        description: str = Form(...),
        photo: str = Form(...),
        release_year: int = Form(...),
        director: str = Form(...),
        duration: int = Form(...),
        genre_id: int = Form(...),

):
    try:
        existing_movie = await MovesCRUD.get_movie(session, title=title)
        if existing_movie:
            return JSONResponse(status_code=400,
                                content={"error": "Фильм с таким названием уже существует."})

        new_movie = MoveCreateSchema(
            title=title,
            description=description,
            photo=photo,
            release_year=release_year,
            director=director,
            duration=duration,
            genre_id=genre_id,
        )
        movie = await MovesCRUD.create_movies(session, new_movie)
        if not movie:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании пользователя, попробуйте еще раз..."})
        logger.info("Фильм %s успешно добавлен", movie.title)
        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Фильм успешно добавлен",
            "data": {
                "title": movie.title,
            }
        })

    except Exception as exc:
        logger.error(f'Ошибка при создании пользователя: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})




@moves_router.get(
    path="get_movies",
    summary="Получить все фильмы",
    response_description="Список фильмов"
)
async def get_movies(session: AsyncSession = Depends(get_db)):
    try:
        movies = await MovesCRUD.get_movie(session)
        if not movies:
            return JSONResponse(status_code=404,
                                content={"error": "Фильм не найден."})
        logger.info("Фильм получен")
        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Фильм получен",
            "data": {
                "movies": movies,
            }
        })

    except Exception as exc:
        logger.error(f'Ошибка поиске фильма: %s', exc)
