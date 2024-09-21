from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.Users.crud import (
    get_users,
    get_user_by_email,
    get_user_by_phone,
    get_user_by_login
)
from src.Users.schemas import User


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
async def get_all_users(db: AsyncSession = Depends(get_db)):
    try:
        users = await get_users(db)
        if not users:
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
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователей: {e}"})


@router.get(
    "/user/by_email/{email}",
    response_model=User,
    summary="Получение пользователя по его email",
    response_description="Конкретный пользователь"
    )
async def get_current_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    try:
        user_db_email = await get_user_by_email(db, email=email)
        if user_db_email is None:
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = [
            {
                "id": user.id,
                "login": user.username,
                "email": user.email,
                "phone": user.phone,
            }
            for user in user_db_email
        ]
        return JSONResponse(status_code=200, content={"user": user_data})

    except Exception as e:
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})



@router.get(
    "/user/by_phone/{phone}",
    response_model=User,
    summary="Получение пользователя по его телефону",
    response_description="Конкретный пользователь"
    )
async def get_current_user_by_phone(phone: str, db: AsyncSession = Depends(get_db)):
    try:
        user_phone = await get_user_by_phone(db, phone=phone)
        if user_phone is None:
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = [
            {
                "id": user.id,
                "login": user.username,
                "email": user.email,
                "phone": user.phone,
            }
            for user in user_phone
        ]

        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})


@router.get(
    "/user/by_login/{login}",
    response_model=User,
    summary="Получение пользователя по его логину",
    response_description="Конкретный пользователь"
    )
async def get_current_user_by_login(login: str, db: AsyncSession = Depends(get_db)):
    try:
        user_login = await get_user_by_login(db, username=login)
        if user_login is None:
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = [
            {
                "id": user.id,
                "login": user.username,
                "email": user.email,
                "phone": user.phone,
            }
            for user in user_login
        ]

        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})
