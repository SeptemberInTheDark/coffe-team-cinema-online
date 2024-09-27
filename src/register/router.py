import os
import re
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.Users.crud import UserCRUD

from src.Users.schemas import UserCreate
from src.Users.manager import UserHashManager
from src.utils.logging import AppLogger

from config import settings

logger = AppLogger().get_logger()


router = APIRouter(
    prefix='/api/register',
    tags=['Регистрация пользователя']
)


@router.post("")
async def user_registration(
        username: str = Form(..., min_length=3),
        password: str = Form(..., min_length=3),
        email: str = Form(...),
        phone: str = Form(...),

        db: AsyncSession = Depends(get_db)
):
    try:
        if not re.match(settings.EMAIL_VALIDATOR, email):
            logger.error('Некорректный email')
            return JSONResponse(status_code=400, content={"error": "Некорректный email"})

        if not re.match(settings.PHONE_VALIDATOR, phone):
            logger.error('Некорректный номер телефона')
            return JSONResponse(status_code=400, content={"error": "Некорректный номер телефона"})

        user_salt = os.urandom(32).hex()
        hashed_password = UserHashManager.hash_str(password, user_salt)

        existing_user = await UserCRUD.check_user(db, username, email, phone)
        if existing_user:
            return JSONResponse(status_code=400,
                                content={"error": "Пользователь с таким именем или почтой уже существует."})

        new_user = UserCreate(
            username=username,
            email=email,
            phone=phone,
            hashed_password=hashed_password
        )
        user = await UserCRUD.create_user(db=db, user=new_user)

        if not user:
            return JSONResponse(status_code=400,
                                content={"error": "Ошибка при создании пользователя, попробуйте еще раз..."})
        logger.info(f"Пользователь {user.username} успешно зарегистрирован")

        return JSONResponse(status_code=201, content={
            "success": True,
            "message": "Пользователь успешно зарегистрирован",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email
            }
        })

    except Exception as exc:
        logger.error(f'Ошибка при создании пользователя: {exc}')
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})
