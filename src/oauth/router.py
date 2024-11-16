from fastapi import APIRouter
from src.oauth.providers.google import router as google_router
from src.oauth.providers.yandex import router as yandex_router
from src.oauth.providers.vk import router as vk_router
from config import settings

router = APIRouter(prefix=settings.API_OAuth_PREFIX)

router.include_router(google_router, prefix="/google", tags=["Google OAuth"])
router.include_router(yandex_router, prefix="/yandex", tags=["Yandex OAuth"])
router.include_router(vk_router, prefix="/vk", tags=["VK OAuth"])
