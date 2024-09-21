
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from .manager import UserHashManager
import os
from typing import List, Optional


class UserCRUD:

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
        return await db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) ->List[models.User]:
        return await db.query(models.User).filter(models.User.email == email).all()

    @staticmethod
    async def get_user_by_phone(db: AsyncSession, phone: str) -> List[models.User]:
        return await db.query(models.User).filter(models.User.phone == phone).all()

    @staticmethod
    async def get_user_by_login(db: AsyncSession, username: str) -> List[models.User]:
        return await db.query(models.User).filter(models.User.username == username).all()

    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 20):
        return await db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    async def check_user(db: AsyncSession, username: str, email: str, phone: str) -> Optional[models.User]:
        try:
            existing_user = await db.query(models.User).filter(
                (models.User.username == username) |
                (models.User.email == email) |
                (models.User.phone == phone)
            ).first()
            return existing_user if existing_user else None
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
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
