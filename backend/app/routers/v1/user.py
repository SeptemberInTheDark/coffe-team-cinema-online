from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.core.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_user import UserCRUD

from app.schemas.User import User
from app.utils.logging import AppLogger


logger = AppLogger().get_logger()

router = APIRouter()


@router.get(
    "",
    response_model=User,
    summary="Получить всех пользователей",
    response_description="Список пользователей"

    )
async def get_all_users(db: AsyncSession = Depends(get_db)):
    try:
        users = await UserCRUD.get_users(db)
        if not users:
            logger.info('Ни одного пользователя не найдено, либо не существует')

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

async def get_current_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    try:
        user_db_email = await UserCRUD.get_user(db, email=email)
        if user_db_email is None:
            logger.info("Пользователь по email %s не найден", email)
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

async def get_current_user_by_phone(phone: str, db: AsyncSession = Depends(get_db)):
    try:
        user_phone = await UserCRUD.get_user(db, phone=phone)
        if user_phone is None:
            logger.info("Пользователь по телефону %s не найден", phone)
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = {
                "id": user_phone.id,
                "login": user_phone.username,
                "email": user_phone.email,
                "phone": user_phone.phone,
            }


        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        logger.error("Ошибка при получении пользователя по phone:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})


@router.get(
    "/user/by_login/{login}",
    response_model=User,
    summary="Получение пользователя по его логину",
    response_description="Конкретный пользователь"
    )

async def get_current_user_by_login(login: str, db: AsyncSession = Depends(get_db)):
    try:
        user_login = await UserCRUD.get_user(db, username=login)
        if user_login is None:
            logger.info("Пользователь по логину %s не найден", login)
            return JSONResponse(status_code=400, content={"error": "Пользователь не найден"})

        user_data = {
                "id": user_login.id,
                "login": user_login.username,
                "email": user_login.email,
                "phone": user_login.phone,
            }

        return JSONResponse(status_code=200, content={"user": user_data})
    except Exception as e:
        logger.error("Ошибка при получении пользователя по login:\n %s", e)
        raise HTTPException(status_code=500, detail={f"Ошибка при получении пользователя: {e}"})
