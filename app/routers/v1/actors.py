from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.models.actor import Actor
from app.crud.crud_actors import ActorsCRUD
from app.schemas.Actor import ActorCreateSchema, ActorResponseSchema, ActorUpdateSchema
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


@router.delete(
    path="/delete_actor",
    summary="Удалить актёра",
    response_description="Удаленный актёра"
)
async def delete_actor(session: AsyncSession = Depends(get_db),
                       actor_id: int = Form(...)):
    try:
        deleted = await ActorsCRUD.delete_actor(session, id=actor_id)
        if deleted:
            logger.info("Актёр %s удален", id=actor_id)
            return JSONResponse(status_code=200, content={"message": f"Актёр '{actor_id}' успешно удален."})
        else:
            logger.info("Актёр %s не найден", actor_id)
            return JSONResponse(status_code=404, content={"error": "Актёр не найден."})

    except Exception as exc:
        logger.error('Ошибка при удалении актёра: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})


@router.patch(
    path="/update_actor/{actor_id}",
    summary="Обновить данные актёра",
    response_description="Обновленный актёр",
    status_code=status.HTTP_200_OK
)
async def update_actor_handler(
        actor_id: int,
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        eng_full_name: Optional[str] = Form(None),
        biography: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        height: Optional[int] = Form(None),
        date_of_birth: Optional[date] = Form(None),
        place_of_birth: Optional[str] = Form(None),
        session: AsyncSession = Depends(get_db)
):
    try:
        # Проверяем существование актера
        existing_actor = await session.get(Actor, actor_id)
        if not existing_actor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Актер не найден"
            )

        update_actor_data = ActorUpdateSchema(
            first_name=first_name if first_name is not None else existing_actor.first_name,
            last_name=last_name if last_name is not None else existing_actor.last_name,
            eng_full_name=eng_full_name if eng_full_name is not None else existing_actor.eng_full_name,
            biography=biography if biography is not None else existing_actor.biography,
            avatar=avatar if avatar is not None else existing_actor.avatar,
            height=height if height is not None else existing_actor.height,
            date_of_birth=date_of_birth if date_of_birth is not None else existing_actor.date_of_birth,
            place_of_birth=place_of_birth if place_of_birth is not None else existing_actor.place_of_birth
        )

        # Обновляем актёра
        updated_actor = await ActorsCRUD.update_actor(
            session=session,
            actor_id=actor_id,
            actor_data=update_actor_data
        )

        # # Обновляем актера с помощью универсального метода
        # updated_actor = await ActorsCRUD.update_entity(
        #     session=session,
        #     entity_id=actor_id,
        #     entity_class=Actor,
        #     update_data=update_actor_data,
        #     entity_name="актера"
        # )

        if not updated_actor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при обновлении актера"
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": form_actors_data([updated_actor])[0]
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
        logger.error(f"Ошибка при обновлении актера: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
