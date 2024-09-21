from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.Users.crud import check_user, create_user
from src.Users.schemas import UserCreate
import os
from src.Users.manager import UserHashManager

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
        user_salt = os.urandom(32).hex()
        hashed_password = UserHashManager.hash_str(password, user_salt)
        existing_user = await check_user(db, username, email, phone)

        if existing_user:
            return JSONResponse(status_code=400, content={"error":"Пользователь с таким именем или почтой уже существует."})


        new_user = UserCreate(
            username=username,
            email=email,
            phone=phone,
            hashed_password=hashed_password
        )
        user = await create_user(db=db, user=new_user)

        if not user:
            return JSONResponse(status_code=400, content={"error": "Ошибка при создании пользователя, попробуйте еще раз ..."})

        print('user: ', user)
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
        raise http_exc


