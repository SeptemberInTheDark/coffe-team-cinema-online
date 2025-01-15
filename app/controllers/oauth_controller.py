from abc import ABC, abstractmethod
from fastapi import HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.init_db import get_db
from backend.app.crud.crud_user import UserCRUD
from backend.app.schemas.User import UserCreate
from backend.app.utils.manager import user_hash_manager
from .jwt_controller import JWTManager
from backend.app.utils.logging import AppLogger
import httpx
import secrets

logger = AppLogger().get_logger()


class OAuthProvider(ABC):
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.authorize_url = None
        self.token_url = None
        self.user_info_url = None
        self.scope = None

    @abstractmethod
    async def get_authorization_url(self):
        pass

    @abstractmethod
    async def get_user_info(self, token_data):
        pass

    async def login(self):
        auth_url = await self.get_authorization_url()
        return RedirectResponse(url=auth_url)

    async def callback(self, code: str, db: AsyncSession = Depends(get_db)):
        """
        Обработка колбэка OAuth
        """
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data)
            if response.status_code != 200:
                logger.error(f"Token error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Token error: {response.text}",
                )
            token_data = response.json()

        user_info = await self.get_user_info(token_data)
        email = user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by OAuth provider.")

        existing_user = await UserCRUD.get_user(db, email=email)

        if existing_user:
            logger.info(f"Пользователь с email {email} уже существует.")
            access_token = JWTManager.encode_jwt({"sub": existing_user.email})
            refresh_token = JWTManager.generate_refresh_token({"sub": existing_user.email})
        else:
            random_password = secrets.token_urlsafe(16)
            new_user_data = UserCreate(
                username=user_info.get("name") or email.split("@")[0],
                email=email,
                phone="",
                hashed_password=user_hash_manager.hash_password(random_password),
                is_active=True,
            )

            new_user = await UserCRUD.create_user(db=db, user=new_user_data)

            if not new_user:
                logger.error("Ошибка при создании пользователя через OAuth.")
                return JSONResponse(
                    status_code=500, content={"error": "Ошибка при создании пользователя."}
                )

            logger.info(f"Новый пользователь {new_user.username} создан через OAuth.")
            access_token = JWTManager.encode_jwt({"sub": new_user.email})
            refresh_token = JWTManager.generate_refresh_token({"sub": new_user.email})

        return JSONResponse(
            content={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "redirect_url": "/",
            }
        )
