from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.crud.crud_movies import MovesCRUD
from app.models import movie
from app.schemas.Movie import MoveCreateSchema, MovieResponseSchema, MovieUpdateSchema
from fastapi.responses import JSONResponse

from app.utils.form_movies import form_movies_data
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.post(
    path="/add_movie",
    summary="Добавить фильм",
    response_description="Добавленный фильм",
    status_code=status.HTTP_201_CREATED,
)
async def add_movie(
        session: AsyncSession = Depends(get_db),
        title: str = Form(...),
        eng_title: str = Form(None),
        url: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        release_year: Optional[date] = Form(None),
        director: Optional[str] = Form(None),
        country: Optional[str] = Form(None),
        part: Optional[int] = Form(None),
        age_restriction: Optional[int] = Form(None),
        duration: Optional[int] = Form(None),
        category_id: Optional[int] = Form(None),
        producer: Optional[List[str]] = Form(None),
        screenwriter: Optional[List[str]] = Form(None),
        operator: Optional[List[str]] = Form(None),
        composer: Optional[List[str]] = Form(None),
        actors: Optional[List[str]] = Form(None),
        editor: Optional[List[str]] = Form(None),
        genres: Optional[List[int]] = Form(None),
):
    try:
        # Проверка на существующий фильм
        existing_movie = await MovesCRUD.get_movie(session, title=title)
        if existing_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Фильм с таким названием уже существует.",
            )

        # Создаем объект схемы Pydantic
        new_movie_data = MoveCreateSchema(
            title=title,
            url=url,
            eng_title=eng_title,
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
            genres=genres,
        )

        # Создаем фильм
        new_movie = await MovesCRUD.create_movies(session, new_movie_data)
        if not new_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании фильма, попробуйте еще раз...",
            )

        logger.info("Фильм %s успешно добавлен", new_movie.title)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "data": form_movies_data([new_movie])[0]
            }
        )

    except HTTPException as e:
        logger.error("Ошибка при добавлении фильма: %s", e.detail)
        raise e
    except Exception as e:
        logger.error("Ошибка при добавлении фильма: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера. Попробуйте позже.",
        )


@router.patch(
    path="/update_movie/{movie_id}",
    summary="Обновить данные фильма",
    response_description="Обновленный фильм",
    status_code=status.HTTP_200_OK
)
async def update_movie_handler(
        movie_id: int,
        movie_data: MovieUpdateSchema,
        session: AsyncSession = Depends(get_db),
):
    try:
        # Проверяем существование фильма
        existing_movie = await session.get(movie.Movie, movie_id)
        if not existing_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фильм не найден"
            )

        # Обновляем фильм
        updated_movie = await MovesCRUD.update_movie(
            session=session,
            movie_id=movie_id,
            movie_data=movie_data
        )

        if not updated_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при обновлении фильма"
            )

        # Формируем ответ
        movies_data = form_movies_data([updated_movie])

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": form_movies_data([updated_movie])[0]
            }
        )

    except HTTPException as e:
        raise e
    except ValueError as e:
        logger.error(f"Ошибка валидации: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении фильма: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.get(
    path="/get_movies",
    summary="Получить все фильмы",
    response_description="Список фильмов"
)
async def get_movies(session: AsyncSession = Depends(get_db)):
    movies = await MovesCRUD.get_all_movies(session)
    return JSONResponse(
        status_code=200,
        content={"movies": form_movies_data(movies)}
    )


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
    movies_data = form_movies_data(movies)
    return JSONResponse(status_code=200, content={
        "movies": movies_data
    })


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
        # Получаем список объектов Movie
        movies = await MovesCRUD.search_movies_by_genre(session, genre_name=genre)

        if not movies:
            logger.info('Фильмы не найдены')
            return JSONResponse(
                status_code=404,
                content={"error": "Фильмы не найдены."}
            )

        # Предполагаем, что form_movies_data принимает список Movie
        movies_data = form_movies_data(movies)

        logger.info("Фильмы получены")
        return JSONResponse(
            status_code=200,
            content={"movies": movies_data}
        )

    except Exception as exc:
        logger.error('Ошибка при поиске фильмов: %s', exc)
        return JSONResponse(
            status_code=500,
            content={"error": "Внутренняя ошибка сервера."}
        )


@router.get(
    path="/get_movie_by_title",
    summary="Получить фильм по названию",
    response_description="Данные фильма"
)
async def get_movie_by_title(title: str, session: AsyncSession = Depends(get_db)):
    mov = await MovesCRUD.get_movie(session, title=title)
    if not mov:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return JSONResponse(
        status_code=200,
        content=form_movies_data([mov])[0]
    )


@router.get(
    path="/filter_movies",
    summary="Фильтрация фильмов",
    response_description="Отфильтрованный список фильмов"
)
async def filter_movies(
        session: AsyncSession = Depends(get_db),
        title: Optional[str] = Query(None),
        release_year: Optional[int] = Query(None),
        director: Optional[str] = Query(None),
        country: Optional[str] = Query(None),
        age_restriction: Optional[int] = Query(None, ge=0, le=21),
        category_id: Optional[int] = Query(None),
        genres: Optional[List[int]] = Query(None),
        min_duration: Optional[int] = Query(None, description="Минимальная длительность в минутах"),
        max_duration: Optional[int] = Query(None, description="Максимальная длительность в минутах"),
        created_after: Optional[datetime] = Query(
            None,
            description="Фильтр по дате создания (>=), формат: YYYY-MM-DDTHH:MM:SS"
        ),
        created_before: Optional[datetime] = Query(
            None,
            description="Фильтр по дате создания (<=), формат: YYYY-MM-DDTHH:MM:SS"
        ),
        sort_by: Optional[str] = Query(
            None,
            description="Поле для сортировки (created_at, release_year, duration, title)"
        ),
        sort_order: str = Query(
            "asc",
            description="Направление сортировки: asc/desc",
            regex="^(asc|desc)$"
        ),
        skip: int = 0,
        limit: int = 20
):
    try:
        movies = await MovesCRUD.filter_movies(
            session=session,
            title=title,
            release_year=release_year,
            director=director,
            country=country,
            age_restriction=age_restriction,
            category_id=category_id,
            genres=genres,
            min_duration=min_duration,
            max_duration=max_duration,
            created_after=created_after,  # Добавлено
            created_before=created_before,  # Добавлено
            sort_by=sort_by,  # Добавлено
            sort_order=sort_order,  # Добавлено
            skip=skip,
            limit=limit
        )

        if not movies:
            return JSONResponse(
                status_code=404,
                content={"message": "Фильмы не найдены"}
            )

        movies_data = form_movies_data(movies)
        return JSONResponse(
            status_code=200,
            content={"movies": movies_data}
        )

    except Exception as e:
        logger.error(f"Ошибка фильтрации: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Ошибка при фильтрации фильмов"
        )


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
