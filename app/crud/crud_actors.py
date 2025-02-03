from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.actor import Actor
from app.schemas.Actor import ActorCreateSchema
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


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

    # @staticmethod
    # async def delete_actor(session: AsyncSession, **kwargs) -> bool:
    #     delete_actor = await session.get(models.Actor, **kwargs)
    #     if delete_actor:
    #         await session.delete(delete_actor)
    #         await session.commit()
    #         return True
    #     else:
    #         return False
    #
    # @staticmethod
    # async def update_actor(session: AsyncSession, **kwargs) -> Optional[models.Actor | bool]:
    #     update_actor = await session.get(models.Actor, **kwargs)
    #     if update_actor:
    #         update_actor.first_name = kwargs['first_name']
    #         update_actor.last_name = kwargs['last_name']
    #         await session.commit()
    #         await session.refresh(update_actor)
    #         return update_actor
    #     else:
    #         return False
