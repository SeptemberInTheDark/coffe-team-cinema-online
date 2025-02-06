from typing import Optional, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from app.models.actor import Actor
from app.schemas.Actor import ActorCreateSchema, ActorUpdateSchema
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()
Base = declarative_base()


class ActorsCRUD:
    @staticmethod
    async def get_actor(session: AsyncSession, **kwargs) -> Optional[Actor]:
        query = select(Actor).filter_by(**kwargs)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_actors_filter(session: AsyncSession, skip: int = 0, limit: int = 20, **kwargs):
        result = await session.scalars(select(Actor).filter_by(**kwargs).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def get_all_actors(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(Actor).offset(skip).limit(limit))
        return result.all()

    @staticmethod
    async def create_actor(session: AsyncSession, actor_data: ActorCreateSchema) -> Optional[Actor]:
        try:
            new_actor = Actor(
                first_name=actor_data.first_name,
                last_name=actor_data.last_name,
                eng_full_name=actor_data.eng_full_name,
                biography=actor_data.biography,
                avatar=actor_data.avatar,
                height=actor_data.height,
                date_of_birth=actor_data.date_of_birth,
                place_of_birth=actor_data.place_of_birth
            )

            session.add(new_actor)
            await session.commit()
            await session.refresh(new_actor)
            return new_actor

        except Exception as e:
            await session.rollback()
            logger.error("Ошибка при создании актёра: %s", str(e))
            return None

    @staticmethod
    async def delete_actor(session: AsyncSession, **kwargs) -> bool:
        actor = await session.scalar(select(Actor).filter_by(**kwargs))
        if actor:
            await session.delete(actor)
            await session.commit()
            return True
        else:
            return False

    @staticmethod
    async def update_actor(
            session: AsyncSession,
            actor_id: int,
            actor_data: ActorUpdateSchema
    ) -> Optional[Actor]:
        try:
            # Получаем актера по ID
            existing_actor = await session.get(Actor, actor_id)
            if not existing_actor:
                return None

            # Преобразуем данные схемы в словарь, исключая не переданные поля
            update_data = actor_data.model_dump(exclude_unset=True)

            # Обновляем поля актера
            for field, value in update_data.items():
                setattr(existing_actor, field, value)

            # Сохраняем изменения в базе данных
            await session.commit()
            await session.refresh(existing_actor)
            return existing_actor

        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении актера: {str(e)}")
            return None

    @staticmethod
    async def update_entity(
            session: AsyncSession,
            entity_id: int,
            entity_class: Type[Base],
            update_data: BaseModel,
            entity_name: str = "актера"
    ) -> Optional[Base]:
        """
        Универсальный метод для обновления сущности.

        :param session: Сессия базы данных.
        :param entity_id: ID сущности.
        :param entity_class: Класс сущности (например, Actor).
        :param update_data: Данные для обновления (Pydantic схема).
        :param entity_name: Название сущности для логов (например, "актер").
        :return: Обновленная сущность или None, если произошла ошибка.
        """
        try:
            # Получаем сущность по ID
            existing_entity = await session.get(entity_class, entity_id)
            if not existing_entity:
                return None

            # Преобразуем данные схемы в словарь, исключая не переданные поля
            data_to_update = update_data.model_dump(exclude_unset=True)

            # Обновляем поля сущности
            for field, value in data_to_update.items():
                setattr(existing_entity, field, value)

            # Сохраняем изменения в базе данных
            await session.commit()
            await session.refresh(existing_entity)
            return existing_entity

        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении {entity_name}: {str(e)}")
            return None
