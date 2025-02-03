from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.crud.crud_actors import ActorsCRUD
from app.schemas.Actor import ActorCreateSchema, ActorResponseSchema
from fastapi.responses import JSONResponse

from app.utils.form_actors import form_actors_data
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.get(
    path="/get_actors",
    summary="Получить всех актёров",
    response_description="Список актеров"
)
async def get_actors(session: AsyncSession = Depends(get_db)):
    actors = await ActorsCRUD.get_all_actors(session)
    return JSONResponse(
        status_code=200,
        content={"actors": form_actors_data(actors)}
    )


@router.post(
    path="/add_actor",
    summary="Добавить актера",
    response_description="Добавленный актёр",
    status_code=status.HTTP_201_CREATED,
)
async def add_actor(
        session: AsyncSession = Depends(get_db),
        first_name: str = Form(...),
        last_name: str = Form(None),
        eng_full_name: Optional[str] = Form(None),
        biography: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        height: Optional[int] = Form(None),
        date_of_birth: Optional[date] = Form(None),
        place_of_birth: Optional[str] = Form(None),
):
    try:
        # Проверка на существующего актёра
        existing_actor = await ActorsCRUD.get_actor(session, first_name=first_name, last_name=last_name)
        if existing_actor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Актёр с таким именем и фамилией уже существует.",
            )

        # Создаем объект схемы Pydantic
        new_actor_data = ActorCreateSchema(
            first_name=first_name,
            last_name=last_name,
            eng_full_name=eng_full_name,
            biography=biography,
            avatar=avatar,
            height=height,
            date_of_birth=date_of_birth,
            place_of_birth=place_of_birth,
        )

        # Создаем актёра
        new_actor = await ActorsCRUD.create_actor(session, new_actor_data)
        if not new_actor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании актёра, попробуйте еще раз...",
            )

        logger.info("Актёр %s %s успешно добавлен", new_actor.first_name, new_actor.last_name)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "data": ActorResponseSchema.from_orm(new_actor).dict()
            }
        )

    except HTTPException as e:
        logger.error("Ошибка при добавлении актёра: %s", e.detail)
        raise e
    except Exception as e:
        logger.error("Ошибка при добавлении актёра: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера. Попробуйте позже.",
        )
