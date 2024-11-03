import asyncio
import pytest
from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool

from db import get_db, BaseModel
from config import settings
from app import app

# Строка подключения к тестовой базе данных
DATABASE_URL_TEST = "postgresql+asyncpg://postgres:postgres@localhost/test_db"

# Создание асинхронного движка и сессии
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata = BaseModel.metadata
metadata.bind = engine_test

# Переопределение зависимости для получения сессии
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_async_session

# Фикстура для подготовки базы данных
@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)  # Создание всех таблиц
    yield  # Тесты выполняются здесь
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)  # Удаление всех таблиц после тестов

# Фикстура для создания события цикла
@pytest.fixture(scope='session')
def event_loop(request):
    """Создание экземпляра цикла событий по умолчанию для каждого теста."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Асинхронный клиент для тестирования API
@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
