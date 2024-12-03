from fastapi import APIRouter, Depends
from app.core.config import settings
from app.controllers.google_controller import GoogleOAuthProvider
from app.controllers.yandex_controller import YandexOAuthProvider
from app.controllers.vk_controller import VKOAuthProvider
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.init_db import get_db

google_provider = GoogleOAuthProvider()
yandex_provider = YandexOAuthProvider()
vk_provider = VKOAuthProvider()

router = APIRouter(prefix=settings.API_OAuth_PREFIX)


# Google OAuth
@router.get("/google/login", tags=["Google OAuth"])
async def google_login():
    """
    Начало авторизации через Google.
    """
    return await google_provider.login()


@router.get("/google/callback", tags=["Google OAuth"])
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """
    Обработка колбэка Google.
    """
    return await google_provider.callback(code, db)


# Yandex OAuth
@router.get("/yandex/login", tags=["Yandex OAuth"])
async def yandex_login():
    """
    Начало авторизации через Yandex.
    """
    return await yandex_provider.login()


@router.get("/yandex/callback", tags=["Yandex OAuth"])
async def yandex_callback(code: str, db: AsyncSession = Depends(get_db)):
    """
    Обработка колбэка Yandex.
    """
    return await yandex_provider.callback(code, db)


# VK OAuth
@router.get("/vk/login", tags=["VK OAuth"])
async def vk_login():
    """
    Начало авторизации через VK.
    """
    return await vk_provider.login()


@router.get("/vk/callback", tags=["VK OAuth"])
async def vk_callback(code: str, db: AsyncSession = Depends(get_db)):
    """
    Обработка колбэка VK.
    """
    return await vk_provider.callback(code, db)
