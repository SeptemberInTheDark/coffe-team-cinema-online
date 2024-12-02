from fastapi import APIRouter
from app.core.config import settings
from app.routers.router import v1 as reg



route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)
route.include_router(reg)
