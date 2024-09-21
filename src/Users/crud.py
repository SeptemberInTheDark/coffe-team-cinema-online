import os
import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .manager import UserHashManager

logger = logging.getLogger(__name__)


async def get_user(session: AsyncSession, user_id: int):
    return await session.scalar(select(models.User).where(models.User.id == user_id))


async def get_user_by_email(session: AsyncSession, email: str):
    return await session.scalar(select(models.User).where(models.User.email == email))


async def get_user_by_phone(session: AsyncSession, phone: str):
    return await session.scalar(select(models.User).where(models.User.phone == phone))


async def get_user_by_login(session: AsyncSession, username: str):
    return await session.scalar(select(models.User).where(models.User.username == username))


async def get_users(session: AsyncSession, skip: int = 0, limit: int = 20):
    result = await session.scalars(select(models.User).offset(skip).limit(limit))
    return result.all()


async def check_user(session: AsyncSession, username: str, email: str, phone: str):
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


async def create_user(session: AsyncSession, user: schemas.UserCreate):
    user_salt = os.urandom(32).hex()
    hashed_password = UserHashManager.hash_str(user.hashed_password, user_salt)

    db_user = models.User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    session.add(db_user)

    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError as error:
        logger.error("%s\nПользователь уже существует", error)
        await session.rollback()

#На потом
def update_user_info():
    pass
