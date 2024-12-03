from fastapi import status, HTTPException
import jwt
from datetime import datetime, timedelta
from app.core.config import settings as global_settings


class JWTManager:
    @staticmethod
    def encode_jwt(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
        """
        Создаёт access токен
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, global_settings.SECRET_KEY, algorithm=global_settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_jwt(token: str):
        """
        Декодирует JWT токен
        """
        try:
            payload = jwt.decode(
                token, global_settings.SECRET_KEY, algorithms=[global_settings.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истёк",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
            )

    @staticmethod
    def generate_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=3)):
        """
        Создаёт refresh токен
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        refresh_jwt = jwt.encode(
            to_encode, global_settings.SECRET_KEY, algorithm=global_settings.ALGORITHM
        )
        return refresh_jwt
