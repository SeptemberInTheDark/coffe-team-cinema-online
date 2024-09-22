import os
import logging

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import JSONResponse

from db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from src.Users.crud import check_user, create_user
from src.Users.schemas import UserCreate
from src.Users.manager import UserHashManager

logger = logging.getLogger(__name__)

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
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user_salt = os.urandom(32).hex()
        hashed_password = UserHashManager.hash_str(password, user_salt)
        existing_user = await check_user(session, username, email, phone)
        if existing_user:
            return JSONResponse(status_code=400, content={"error": "Пользователь с таким"
                                                                   " именем или почтой уже существует."})

        new_user = UserCreate(
            username=username,
            email=email,
            phone=phone,
            hashed_password=hashed_password
        )
        user = await create_user(session=session, user=new_user)

        if not user:
            return JSONResponse(status_code=400, content={"error": "Ошибка при создании "
                                                                   "пользователя, попробуйте еще раз ..."})
        logger.info("user: ", user)
        return JSONResponse(status_code=200, content={
            "success": True,
            "message": "Пользователь успешно зарегистрирован",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email
            }
        })

    except Exception as http_exc:
        logging.error("Unexpected error: %e", http_exc)
        raise HTTPException(status_code=500, detail="Internal server error")
