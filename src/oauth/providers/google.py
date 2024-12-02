import httpx
from fastapi import HTTPException
from src.utils.logging import AppLogger
from .base import OAuthProvider
from config import settings as global_settings

logger = AppLogger().get_logger()


class GoogleOAuthProvider(OAuthProvider):
    def __init__(self):
        super().__init__()
        self.client_id = global_settings.GOOGLE_CLIENT_ID
        self.client_secret = global_settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = global_settings.GOOGLE_REDIRECT_URI
        self.authorize_url = "https://accounts.google.com/o/oauth2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        self.scope = "openid email profile"

    async def get_authorization_url(self):
        return (
            f"{self.authorize_url}"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code&scope={self.scope}"
        )

    async def get_user_info(self, token_data):
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.user_info_url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Google user info error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Google user info error: {response.text}",
                )
            return response.json()
