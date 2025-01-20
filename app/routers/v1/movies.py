from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.crud.crud_movies import MovesCRUD
from app.schemas.Movie import MoveCreateSchema, MovieResponseSchema
from fastapi.responses import JSONResponse

from app.utils.form_movies import form_movies_data, parse_list_field
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
        # Проверка на существующий фильм
        existing_movie = await MovesCRUD.get_movie(session, title=title)
        if existing_movie:
            return JSONResponse(status_code=400,
                                content={"error": "Фильм с таким названием уже существует."})

        # Создаем объект схемы Pydantic
        new_movie_data = MoveCreateSchema(
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

        new_movie = await MovesCRUD.create_movies(session, new_movie_data)

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

    except Exception as e:
        logger.error("Ошибка при добавлении фильма: %s", e)
        return JSONResponse(status_code=500,
                            content={"error": "Произошла ошибка сервера. Попробуйте позже."})


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


from datetime import date

import json


@router.get(
    path="/search_movies_by_title_and_description",
    summary="Получить фильмы по ключевому запросу",
    response_description="Список фильмов"
)
async def get_movies_by_title_and_description(
        query: str = Query(..., description="Ключевое слово для поиска"),
        session: AsyncSession = Depends(get_db)
):
    movies = await MovesCRUD.search_movies(session, query=query)
    if not movies:
        raise HTTPException(status_code=404, detail="Фильмы не найдены")
    movies_data = [
        MovieResponseSchema(
            **{
                **movie.__dict__,
                "release_year": movie.release_year.isoformat() if movie.release_year else None,
                "operator": parse_list_field(movie.operator),
                "composer": parse_list_field(movie.composer),
                "actors": parse_list_field(movie.actors),
                "editor": parse_list_field(movie.editor),
            }
        )
        for movie in movies
    ]
    return {"movies": movies_data}


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
    response_model=MovieResponseSchema,
    response_description="Список фильмов"
)
async def get_movie_by_title(title: str, session: AsyncSession = Depends(get_db)) -> MovieResponseSchema:
    try:
        # Получение фильма из базы данных
        movie = await MovesCRUD.get_movie(session, title=title)
        if movie is None:
            logger.info("Фильм '%s' не найден", title)
            raise HTTPException(status_code=404, detail="Фильм не найден")

        # Преобразование данных для схемы
        movie_data = MovieResponseSchema(
            id=movie.id,
            title=movie.title,
            eng_title=movie.eng_title,
            url=movie.url,
            description=movie.description,
            avatar=movie.avatar,
            release_year=movie.release_year.isoformat() if movie.release_year else None,
            director=movie.director,
            country=movie.country,
            part=movie.part,
            age_restriction=movie.age_restriction,
            duration=movie.duration,
            category_id=movie.category_id,
            producer=movie.producer,
            screenwriter=movie.screenwriter,
            operator=parse_list_field(movie.operator),
            composer=parse_list_field(movie.composer),
            actors=parse_list_field(movie.actors),
            editor=parse_list_field(movie.editor),
        )

        return movie_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Ошибка при получении фильма '%s': %s", title, e)
        raise HTTPException(status_code=500, detail=f"Ошибка при получении фильма: {e}")


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
