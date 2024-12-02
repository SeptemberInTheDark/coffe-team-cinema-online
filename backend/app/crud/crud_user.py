from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.utils.manager import user_hash_manager
from typing import Optional, Tuple
from src.utils.logging import AppLogger

logger = AppLogger().get_logger()



class UserCRUD:
    @staticmethod
    async def get_user(db: AsyncSession, **kwargs) -> Optional[User]:
        return await db.scalar(select(User).filter_by(**kwargs))

    @staticmethod
    async def get_users(session: AsyncSession, skip: int = 0, limit: int = 20):
        result = await session.scalars(select(User).offset(skip).limit(limit))
        return result.all()

    async def check_user(session: AsyncSession, username: str, email: str, phone: str) -> Optional[User]:
        try:
            result = await session.execute(
                select(User).where(
                    (username == User.username) |
                    (User.email == email) |
                    (User.phone == phone)
                )
            )
            existing_user = result.scalar_one_or_none()
            return existing_user
        except Exception as e:
            logger.error("Error checking user: %s", e)
            return None

    @staticmethod
    async def get_user_credentials(db: AsyncSession, username:str) -> Optional[Tuple[str, str]]:
        secrets_info = await db.execute(
            select(User.hashed_password)
            .where(User.username == username)
        )
        credentials = secrets_info.scalar_one_or_none()
        return credentials


    @staticmethod
    async def create_user(db: AsyncSession, user: User) -> Optional[User | bool]:
        hashed_password = user_hash_manager.hash_password(user.hashed_password)

        db_user = User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password,
            is_active=user.is_active,
            role_id=2
        )

        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user

        except Exception as e:
            await db.rollback()
            logger.error("Ошибка при создании пользователя: %s", e)
            return False

    # На потом
    def update_user_info():
        pass
