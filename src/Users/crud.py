
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from .manager import UserHashManager
import os


async def get_user(db: AsyncSession, user_id: int):
    return await db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(db: AsyncSession, email: str):
    return await db.query(models.User).filter(models.User.email == email).all()


async def get_user_by_phone(db: AsyncSession, phone: str):
    return await db.query(models.User).filter(models.User.phone == phone).all()


async def get_user_by_login(db: AsyncSession, username: str):
    return await db.query(models.User).filter(models.User.username == username).all()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 20):
    return await db.query(models.User).offset(skip).limit(limit).all()


async def check_user(db: AsyncSession, username: str, email: str, phone: str):
    try:
        existing_user = db.query(models.User).filter(
            (models.User.username == username) |
            (models.User.email == email) |
            (models.User.phone == phone)
        ).first()
        return existing_user if existing_user else None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    user_salt = os.urandom(32).hex()
    hashed_password = UserHashManager.hash_str(user.hashed_password, user_salt)

    db_user = models.User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    user = await db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)
        return await db_user

    except Exception as e:
        await db.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return False

#На потом
def update_user_info():
    pass
