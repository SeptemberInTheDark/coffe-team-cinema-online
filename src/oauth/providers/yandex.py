from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from config import settings

router = APIRouter()


@router.get("/login")
async def login_yandex():
    """
    Начало авторизации через Яндекс.
    """
    yandex_auth_url = (
        f"https://oauth.yandex.ru/authorize"
        f"?response_type=code"
        f"&client_id={settings.YANDEX_CLIENT_ID}"
        f"&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    )
    return RedirectResponse(url=yandex_auth_url)


@router.get("/callback")
async def auth_callback_yandex(code: str):
    """
    Обработка колбэка после авторизации Яндекс.
    """
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "code": code,
        "client_id": settings.YANDEX_CLIENT_ID,
        "client_secret": settings.YANDEX_CLIENT_SECRET,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Yandex token error: {response.text}",
            )
        token_data = response.json()

    return JSONResponse(content={"user": token_data, "redirect_url": "/"})
