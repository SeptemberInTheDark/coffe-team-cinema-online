from fastapi import APIRouter, Depends, Form, HTTPException, Query
from sqlalchemy import Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.crud.crud_movies import MovesCRUD
from app.schemas.Movie import MoveCreateSchema
from fastapi.responses import JSONResponse

from app.utils.form_movies import form_movies_data
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.post(
    path="/add_movie",
    summary="Добавить фильм",
    response_description="Добавленный фильм"
)
async def add_movie(
        session: AsyncSession = Depends(get_db),
        movie_data: MoveCreateSchema = Depends()
):
    try:
        # Проверка на существование фильма с таким названием
        existing_movie = await MovesCRUD.get_movie(session, title=movie_data.title)
        if existing_movie:
            return JSONResponse(status_code=400,
                                content={"error": "Фильм с таким названием уже существует."})

        # Создание нового фильма
        movie = await MovesCRUD.create_movies(session, movie_data)

        if not movie:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании фильма, попробуйте еще раз..."})

        logger.info("Фильм %s успешно добавлен", movie.title)

        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Фильм успешно добавлен",
            "data": {
                "title": movie.title,
            }
        })

    except Exception as exc:
        logger.error('Ошибка при создании фильма: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})


@router.get(
    path="/get_movies",
    summary="Получить все фильмы",
    response_description="Список фильмов"
)
async def get_movies(session: AsyncSession = Depends(get_db)):
    try:
        movies = await MovesCRUD.get_all_movies(session)
        if not movies:
            logger.info('Фильмы не найдены')
            return JSONResponse(status_code=404,
                                content={"error": "Фильмы не найдены."})

        movies_data = form_movies_data(movies)
        logger.info("Фильмы получен")
        return JSONResponse(status_code=200, content={
            "movies": movies_data
        })

    except Exception as exc:
        logger.error('Ошибка поиске фильма: %s', exc)



@router.get(
    path="/search_movies_by_title_and_description",
    summary="Получить фильмы по ключевому запросу",
    response_description="Список фильмов"
)
async def get_movies_by_title_and_description(
        session: AsyncSession = Depends(get_db),
        query: str = Query(...),
                                              ):
    try:
        movies = await MovesCRUD.search_movies(session, query=query)
        if not movies:
            logger.info('Фильмы не найдены')
            return JSONResponse(status_code=404,
                                content={"error": "Фильмы не найдены."})

        movies_data = form_movies_data(movies)
        logger.info("Фильмы получены")
        return JSONResponse(status_code=200, content={
            "movies": movies_data
        })

    except Exception as exc:
        logger.error('Ошибка поиске фильма: %s', exc)


@router.get(
    path="/search_movies_by_genre",
    summary="Получить фильмы по жанру",
    response_description="Список фильмов"
)
async def get_movies_by_genre(
        session: AsyncSession = Depends(get_db),
        genre: str = Query(...),
                                              ):
    try:
        movies = await MovesCRUD.search_movies_by_genre(session, genre_name=genre)
        if not movies:
            logger.info('Фильмы не найдены')
            return JSONResponse(status_code=404,
                                content={"error": "Фильмы не найдены."})

        movies_data = form_movies_data(movies)
        logger.info("Фильмы получены")
        return JSONResponse(status_code=200, content={
            "movies": movies_data
        })

    except Exception as exc:
        logger.error('Ошибка поиске фильма: %s', exc)

@router.get(
    path="/get_movie_by_title",
    summary="Получить фильм по названию",
    response_description="Список фильмов"
)
async def get_movie_by_title(title: str, session: AsyncSession = Depends(get_db)):
    try:
        movie = await MovesCRUD.get_movie(session, title=title)
        if movie is None:
            logger.info("Фильм не найден")
            return JSONResponse(status_code=404, content={"error": "Фильм не найден"})

        movie_data = {
            "title": movie.title,
            "url_movie": movie.url_movie,
            "description": movie.description,
            "photo": movie.photo,
            "release_year": movie.release_year,
            "director": movie.director,
            "actors": movie.actors,
            "duration": movie.duration,
            "genre_name": movie.genre_name,
        }
        return JSONResponse(status_code=200, content={"movie": movie_data})
    except Exception as e:
        logger.error("Ошибка при получении фильма:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})


@router.delete(
    path="/delete_movie",
    summary="Удалить фильм",
    response_description="Удаленный фильм"
)
async def delete_movie(session: AsyncSession = Depends(get_db),
                       title: str = Form(...)):

    try:
        deleted = await MovesCRUD.delete_movie(session, title=title)
        if deleted:
            logger.info("Фильм %s удален", title)
            return JSONResponse(status_code=200, content={"message": f"Фильм '{title}' успешно удален."})
        else:
            logger.info("Фильм с названием %s не найден", title)
            return JSONResponse(status_code=404, content={"error": "Фильм не найден."})

    except Exception as exc:
            logger.error('Ошибка при удалении фильма: %s', exc)
            return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})
