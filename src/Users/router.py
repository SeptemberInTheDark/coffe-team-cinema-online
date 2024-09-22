import logging

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from src.Users.crud import (
    get_users,
    get_user_by_email,
    get_user_by_phone,
    get_user_by_login
)
from src.Users.schemas import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api',
    tags=['Получение пользотеля/пользователей'],
)


@router.get(
    "/users",
    response_model=User,
    summary="Получить всех пользователей",
    response_description="Список пользователей"
)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        users = await get_users(session)
        if not users:
            logger.info("Пользователей не найдено")
            return JSONResponse(status_code=200, content={"users": []})

        user_list = [
            {
                "id": user.id,
                "login": user.username,
                "email": user.email,
                "phone": user.phone,
                "is_active": user.is_active
            }
           for user in users
        ]

        return JSONResponse(status_code=200, content={"users": user_list})
    except Exception as e:
        logger.error("Ошибка при получении пользователей:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователей: {e}"})


@router.get(
    "/user/by_email/{email}",
    response_model=User,
    summary="Получение пользователя по его email",
    response_description="Конкретный пользователь"
)
async def get_current_user_by_email(email: str, session: AsyncSession = Depends(get_async_session)):
    try:
        user_db_email = await get_user_by_email(session, email=email)
        if user_db_email is None:
            logger.info("Пользователя по email %s не найдено", email)
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = {
            "id": user_db_email.id,
            "login": user_db_email.username,
            "email": user_db_email.email,
            "phone": user_db_email.phone,
        }
        return JSONResponse(status_code=200, content={"user": user_data})

    except Exception as e:
        logger.error("Ошибка при получении пользователя по email:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})


@router.get(
    "/user/by_phone/{phone}",
    response_model=User,
    summary="Получение пользователя по его телефону",
    response_description="Конкретный пользователь"
)
async def get_current_user_by_phone(phone: str, session: AsyncSession = Depends(get_async_session)):
    try:
        user_phone = await get_user_by_phone(session, phone=phone)
        if user_phone is None:
            logger.info("Пользователя по номеру телефона %s не найдено", phone)
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = {
            "id": user_phone.id,
            "login": user_phone.username,
            "email": user_phone.email,
            "phone": user_phone.phone,
        }
        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})


@router.get(
    "/user/by_login/{login}",
    response_model=User,
    summary="Получение пользователя по его логину",
    response_description="Конкретный пользователь"
)
async def get_current_user_by_login(login: str, session: AsyncSession = Depends(get_async_session)):
    try:
        user_login =await get_user_by_login(session, username=login)
        if user_login is None:
            logger.info("Пользователя по логину %s не найдено", login)
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = {
            "id": user_login.id,
            "login": user_login.username,
            "email": user_login.email,
            "phone": user_login.phone,
        }

        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        logger.error("Ошибка при получении пользователя по логину:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})
