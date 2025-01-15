from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.init_db import get_db
from backend.app.crud.crud_genre import GenreCRUD

from backend.app.schemas.Movie import GenreCreateSchema
from fastapi.responses import JSONResponse

from backend.app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.post(
    path="/add_genre",
    summary="Добавить жанр",
    response_description="Добавленный жанр"
)
async def add_genre(
        session: AsyncSession = Depends(get_db),
        name: str = Form(...),

):
    try:
        existing_genre = await GenreCRUD.get_genre(session, name=name)
        if existing_genre:
            return JSONResponse(status_code=400,
                                content={"error": "Такой жанр уже существует."})

        new_genre = GenreCreateSchema(name=name)

        genre = await GenreCRUD.create_genre(session, new_genre)
        if not genre:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании жанра, попробуйте еще раз..."})
        logger.info("Фильм %s успешно добавлен", genre.name)
        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Жанр успешно добавлен",
            "data": {
                "id": genre.id,
            }
        })

    except Exception as exc:
        logger.error('Ошибка при создании жанра: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})


@router.delete(
    path="/delete_genre",
    summary="Удалить жанр",
    response_description="Удаленный жанр"
)
async def delete_movie(session: AsyncSession = Depends(get_db),
                       name: str = Form(...)):
    try:
        deleted = await GenreCRUD.delete_genre(session, name=name)
        if deleted:
            logger.info("Жанр %s удален", name)
            return JSONResponse(status_code=200, content={"message": f"Жанр '{name}' успешно удален."})
        else:
            logger.info("Жанр с названием %s не найден", name)
            return JSONResponse(status_code=404, content={"error": "Жанр не найден."})

    except Exception as exc:
        logger.error('Ошибка при удалении Жанра: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})
