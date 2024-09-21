from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


DATABASE_URL = (f'postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@'
                f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, autocommit=False, autoflush=False)


class BaseModel(DeclarativeBase):
    metadata = MetaData()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session