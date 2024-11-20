from fastapi import status, HTTPException
import jwt
import secrets
import string
from config import settings as global_settings


class JWTManager():

    @staticmethod
    def encode_jwt(data: dict):
        encode_jwt = jwt.encode(data, global_settings.SECRET_KEY, algorithm=global_settings.ALGORITHM)
        return encode_jwt


    @staticmethod
    def decode_jwt(token: str):
        try:
            payload = jwt.decode(token, global_settings.SECRET_KEY, algorithms=[global_settings.ALGORITHM])
            return payload

        except Exception:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )


    @staticmethod
    def generate_refresh_token(length=32):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
