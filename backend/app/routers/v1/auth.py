from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from backend.app.core.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.crud.crud_user import UserCRUD
from backend.app.utils.manager import user_hash_manager
from backend.app.utils.logging import AppLogger
from backend.app.controllers.jwt_controller import JWTManager
from jose import JWTError
from datetime import timedelta

logger = AppLogger().get_logger()

router = APIRouter()


@router.post("")
async def auth_user(
    username: str = Form(..., min_length=2),
    password: str = Form(..., min_length=2),
    db: AsyncSession = Depends(get_db),
):
    """
    Авторизация пользователя
    """
    try:
        user = await UserCRUD.get_user(db=db, username=username)

        if not user:
            return JSONResponse(
                content={"error": "Пользователь не зарегистрирован"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        hashed_password = await UserCRUD.get_user_credentials(db, username)

        if not hashed_password:
            return JSONResponse(
                content={"error": "Неверный пароль"}, status_code=status.HTTP_401_UNAUTHORIZED
            )

        decode_pass = user_hash_manager.check_password(hashed_password, password)

        if decode_pass:
            access_token = JWTManager.encode_jwt({"sub": username})
            refresh_token = JWTManager.generate_refresh_token({"sub": username})

            response = JSONResponse(
                content={
                    "success": True,
                    "login": True,
                    "username": username,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status_code=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="_key_token",
                value=access_token,
                httponly=True,
                max_age=timedelta(days=3).total_seconds(),
            )
            return response
        else:
            return JSONResponse(
                content={"error": "Неверный пароль"}, status_code=status.HTTP_401_UNAUTHORIZED
            )

    except Exception as e:
        logger.error(f"Ошибка авторизации: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Произошла ошибка на стороне сервера, обратитесь в тех. поддержку.",
                "details": str(e),
            },
        )


@router.post("/token/refresh")
async def refresh_token(refresh_token: str = Form(...)):
    """
    Обновление access токена с использованием refresh токена
    """
    try:
        payload = JWTManager.decode_jwt(refresh_token)
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Недействительный refresh токен")

        access_token = JWTManager.encode_jwt({"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительный refresh токен")
