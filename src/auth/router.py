from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import JSONResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_db
from src.Users.crud import UserCRUD
# from src.Users.models import User as users_db
from sqlalchemy.ext.asyncio import AsyncSession
# import os
# from src.Users.manager import UserHashManager
from src.utils.logging import AppLogger
from .manager import JWTManager
import jwt


logger = AppLogger().get_logger()

router = APIRouter(
    prefix='/api/auth',
    tags=['Авторизация пользователя']
)


@router.post("/login")
async def auth_user(
    username: str = Form(..., min_length=2),
    password: str = Form(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    try:
        if not username or not password:
            return JSONResponse(content={"error": "Логин и пароль обязательны для вввода"}, status_code=status.HTTP_400_BAD_REQUEST)

        user = await UserCRUD.get_user(db, username)
        if not user:
            return JSONResponse(content="Пользователь не зарегистрирован", status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = JWTManager.encode_jwt({"sub": username})

        response = JSONResponse(content={
            "success": True,
            "login": True,
            "password": True,
            "username": username,
        }, status_code=200)

        response.set_cookie(key="accepted_key_token", value=access_token, httponly=True)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



async def get_current_user(request: Request):
    token = request.cookies.get('accepted_key_token')
    if token is None:
        raise HTTPException(status_code=401, detail="Срок действия сессии истёк, пожалуйста, авторизуйтесь заново.")

    try:
        payload = JWTManager.decode_jwt(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Не валидный токен")

        return {"username": username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Не валидный токен")
