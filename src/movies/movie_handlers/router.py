from fastapi import APIRouter
# from fastapi.exceptions import HTTPException
# from fastapi.responses import JSONResponse
# from db import get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.Users.crud import UserCRUD

from src.utils.logging import AppLogger


logger = AppLogger().get_logger()

moves_router = APIRouter(
    prefix='/api',
    tags=['Получение пользотеля/пользователей'],
)