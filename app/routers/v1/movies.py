from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Query
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
        title: str = Form(...),
        url: str = Form(None),
        description: str = Form(...),
        avatar: str = Form(None),
        release_year: date = Form(None),
        director: str = Form(None),
        country: str = Form(None),
        part: int = Form(None),
        age_restriction: int = Form(None),
        duration: int = Form(None),
        category_id: int = Form(None),
        producer: str = Form(None),
        screenwriter: str = Form(None),
        operator: List[str] = Form(None),
        composer: List[str] = Form(None),
        actors: List[str] = Form(None),
        editor: List[str] = Form(None),
):
    try:
        existing_movie = await MovesCRUD.get_movie(session, title=title)
        if existing_movie:
            return JSONResponse(status_code=400,
                                content={"error": "Фильм с таким названием уже существует."})

        new_movie = MoveCreateSchema(
            title=title,
            url=url,
            description=description,
            avatar=avatar,
            release_year=release_year,
            director=director,
            country=country,
            part=part,
            age_restriction=age_restriction,
            duration=duration,
            category_id=category_id,
            producer=producer,
            screenwriter=screenwriter,
            operator=operator,
            composer=composer,
            actors=actors,
            editor=editor,
        )

        if not new_movie:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании фильма, попробуйте еще раз..."})

        logger.info("Фильм %s успешно добавлен", new_movie.title)

        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Фильм успешно добавлен",
            "data": {
                "title": new_movie.title,
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
            "url": movie.url,
            "description": movie.description,
            "avatar": movie.avatar,
            "release_year": movie.release_year,
            "director": movie.director,
            "country": movie.country,
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
