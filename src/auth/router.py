from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import JSONResponse
from db import get_db
from src.Users.crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.logging import AppLogger
from src.auth.manager import JWTManager
from src.Users.manager import user_hash_manager
from jwt.exceptions import JWTException
from datetime import timedelta


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
        user = await UserCRUD.get_user(db=db, username=username)

        if not user:
            return JSONResponse(content={"error": "Пользователь не зарегистрирован"}, status_code=status.HTTP_401_UNAUTHORIZED)

        hashed_password = await UserCRUD.get_user_credentials(db, username)

        if not hashed_password:
            return JSONResponse(content={"error": "Неверный пароль"}, status_code=status.HTTP_401_UNAUTHORIZED)

        decode_pass = user_hash_manager.check_password(hashed_password, password)
        print(f'decode_pass: {decode_pass}')

        if decode_pass:

            access_token = JWTManager.encode_jwt({"sub": username})

            response = JSONResponse(content={
                "success": True,
                "login": True,
                "username": username,
            }, status_code=status.HTTP_200_OK)

            response.set_cookie(
                key="_key_token",
                value=access_token,
                httponly=True,
                max_age=timedelta(days=3).total_seconds()
            )
            return response
        else:
            return JSONResponse(content={"error": "Такого пароля не существует"}, status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Произошла ошибка на стороне сервера, обратитесь в тех. поддержку.", "details": str(e)}
            )


async def get_current_user(request: Request):
    token = request.cookies.get('_key_token')
    if token is None:
        raise HTTPException(status_code=401, detail="Срок действия сессии истёк, пожалуйста, авторизуйтесь заново.")

    try:
        payload = JWTManager.decode_jwt(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Не валидный токен")

        return {"username": username}
    except JWTException:
        raise HTTPException(status_code=401, detail="Не валидный токен")
