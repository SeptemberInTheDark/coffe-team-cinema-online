import os

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from config import settings
from db import get_db
from src.Users.crud import UserCRUD
from src.Users.manager import UserHashManager
from src.Users.reset_pass.reset_pass_utils import is_valid_email, generate_reset_code
from src.Users.schemas import PasswordResetConfirm
from src.utils.logging import AppLogger

logger = AppLogger().get_logger()

redis_client = redis.from_url(url=settings.REDIS_URL, decode_responses=True)

reset_pass_router = APIRouter(
    prefix='/api',
    tags=['Востановление/изменение пароля'],
)


@reset_pass_router.post(
    path='/password-reset/{email}',
    summary="Получение временного кода для восстановления пароля",
    response_description="Email пользователя для восстановления"
)
async def request_password_reset(email: str, db: AsyncSession = Depends(get_db)):
    # Проверка валидности email
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    user = await UserCRUD.get_user(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Генерация кода восстановления
    reset_code = generate_reset_code()

    # Сохраняем код и срок действия во временную базу
    await redis_client.set(f"password_reset:{email}", reset_code, ex=600)

    # Отправляем код на email
    # send_email(email, reset_code)

    logger.info(f"Password reset code sent to {email}")
    return JSONResponse(status_code=200, content={
        "message": "Password reset code sent to " + email,
    })


@reset_pass_router.post(
    path="/password-reset/confirm/",
    response_model=PasswordResetConfirm,
    summary="Подтверждение восстановления пароля",
)
async def confirm_password_reset(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    email = data.email
    reset_code = data.reset_code
    new_password = data.new_password

    # Проверка валидности email
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="email не найден")

    # Получаем код из Redis
    stored_reset_code = await redis_client.get(f"password_reset:{email}")

    if not stored_reset_code:
        raise HTTPException(status_code=400, detail="Код не найден")

    # Проверяем правильность кода
    if stored_reset_code != reset_code:
        raise HTTPException(status_code=400, detail="Введен неверный код")

    # Ищем пользователя в базе данных
    user = await UserCRUD.get_user(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Хэшируем новый пароль
    user_salt = os.urandom(32).hex()
    hashed_password = UserHashManager.hash_str(new_password, user_salt)

    # Обновляем пароль пользователя
    user.hashed_password = hashed_password
    await db.commit()

    # Удаляем код из Redis после успешного восстановления
    await redis_client.delete(f"password_reset:{email}")
    logger.info(f"Password successfully reset for user {email}")
    return JSONResponse(status_code=200, content={
        "message": "Пароль успешно изменен",
    })
