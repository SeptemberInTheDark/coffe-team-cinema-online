import httpx
from fastapi import HTTPException
from backend.app.utils.logging import AppLogger
from .oauth_controller import OAuthProvider
from backend.app.core.config import settings as global_settings

logger = AppLogger().get_logger()


class YandexOAuthProvider(OAuthProvider):
    def __init__(self):
        super().__init__()
        self.client_id = global_settings.YANDEX_CLIENT_ID
        self.client_secret = global_settings.YANDEX_CLIENT_SECRET
        self.redirect_uri = global_settings.YANDEX_REDIRECT_URI
        self.authorize_url = "https://oauth.yandex.ru/authorize"
        self.token_url = "https://oauth.yandex.ru/token"
        self.user_info_url = "https://login.yandex.ru/info"
        self.scope = "login:email login:info"

    async def get_authorization_url(self):
        return (
            f"{self.authorize_url}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )

    async def get_user_info(self, token_data):
        headers = {"Authorization": f"OAuth {token_data['access_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.user_info_url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Yandex user info error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Yandex user info error: {response.text}",
                )
            return response.json()
