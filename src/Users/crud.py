from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from .manager import UserHashManager
import os
from typing import List, Optional
from src.utils.logging import AppLogger

logger = AppLogger().get_logger()

class UserCRUD:

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
        return await db.scalar(select(models.User).where(models.User.id == user_id))

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) ->List[models.User]:
        return await db.scalar(select(models.User).where(models.User.email == email))

    @staticmethod
    async def get_user_by_phone(db: AsyncSession, phone: str) -> List[models.User]:
        return await db.scalar(select(models.User).where(models.User.phone == phone))

    @staticmethod
    async def get_user_by_login(db: AsyncSession, username: str) -> List[models.User]:
        return await db.scalar(select(models.User).where(models.User.username == username))

    @staticmethod
    async def get_users(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(models.User).offset(skip).limit(limit))
        return result.all()

    async def check_user(session: AsyncSession, username: str, email: str, phone: str) -> Optional[models.User]:
        try:
            result = await session.execute(
                select(models.User).where(
                    (models.User.username == username) |
                    (models.User.email == email) |
                    (models.User.phone == phone)
                )
            )
            existing_user = result.scalar_one_or_none()
            return existing_user
        except Exception as e:
            logger.error("Error checking user: %s", e)
            return None

    @staticmethod
    async def create_user(db: AsyncSession, user: schemas.UserCreate) -> Optional[models.User]:
        user_salt = os.urandom(32).hex()
        hashed_password = UserHashManager.hash_str(user.hashed_password, user_salt)

        db_user = models.User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password,
            is_active=user.is_active
        )

        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user

        except Exception as e:
            await db.rollback()
            print(f"Ошибка при создании пользователя: {e}")
            return False

    #На потом
    def update_user_info():
        pass
