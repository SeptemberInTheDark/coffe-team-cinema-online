import httpx
from fastapi import HTTPException
from app.utils.logging import AppLogger
from .oauth_controller import OAuthProvider
from app.core.config import settings as global_settings

logger = AppLogger().get_logger()


class VKOAuthProvider(OAuthProvider):
    def __init__(self):
        super().__init__()
        self.client_id = global_settings.VK_CLIENT_ID
        self.client_secret = global_settings.VK_CLIENT_SECRET
        self.redirect_uri = global_settings.VK_REDIRECT_URI
        self.authorize_url = "https://oauth.vk.com/authorize"
        self.token_url = "https://oauth.vk.com/access_token"
        self.user_info_url = "https://api.vk.com/method/users.get"
        self.scope = "email"

    async def get_authorization_url(self):
        return (
            f"{self.authorize_url}"
            f"?client_id={self.client_id}"
            f"&display=page&redirect_uri={self.redirect_uri}"
            f"&scope={self.scope}&response_type=code&v=5.131"
        )

    async def get_user_info(self, token_data):
        params = {
            "access_token": token_data["access_token"],
            "v": "5.131",
            "fields": "first_name,last_name,email",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.user_info_url, params=params)
            if response.status_code != 200:
                logger.error(f"VK user info error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"VK user info error: {response.text}",
                )
            response_json = response.json()
            if "response" in response_json and len(response_json["response"]) > 0:
                user_info = response_json["response"][0]
                if "email" not in user_info and "email" in token_data:
                    user_info["email"] = token_data["email"]
                return user_info
            else:
                raise HTTPException(status_code=400, detail="Failed to get user info from VK.")
