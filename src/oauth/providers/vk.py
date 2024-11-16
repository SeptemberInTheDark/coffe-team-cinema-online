from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from config import settings

router = APIRouter()


@router.get("/login")
async def login_vk():
    """
    Начало авторизации через ВКонтакте.
    """
    vk_auth_url = (
        f"https://oauth.vk.com/authorize"
        f"?client_id={settings.VK_CLIENT_ID}"
        f"&display=page&redirect_uri={settings.VK_REDIRECT_URI}"
        f"&scope=email&response_type=code&v=5.131"
    )
    return RedirectResponse(url=vk_auth_url)


@router.get("/callback")
async def auth_callback_vk(code: str):
    """
    Обработка колбэка после авторизации ВКонтакте.
    """
    token_url = "https://oauth.vk.com/access_token"
    data = {
        "client_id": settings.VK_CLIENT_ID,
        "client_secret": settings.VK_CLIENT_SECRET,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"VK token error: {response.text}",
            )
        token_data = response.json()

    user_info_url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": token_data["access_token"],
        "v": "5.131",
        "fields": "first_name,last_name,email",
    }

    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(user_info_url, params=params)
        if user_info_response.status_code != 200:
            raise HTTPException(
                status_code=user_info_response.status_code,
                detail=f"VK user info error: {user_info_response.text}",
            )

    user_info = user_info_response.json()
    return JSONResponse(content={"user": user_info, "redirect_url": "/"})
