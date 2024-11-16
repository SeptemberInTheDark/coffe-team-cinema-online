from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from config import settings

router = APIRouter()


@router.get("/login")
async def login_google():
    """
    Начало авторизации через Google.
    """
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code&scope=openid email profile"
    )
    return RedirectResponse(url=google_auth_url)


@router.get("/callback")
async def auth_callback_google(code: str):
    """
    Обработка колбэка после авторизации Google.
    """
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Google token error: {response.text}",
            )
        token_data = response.json()

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(user_info_url, headers=headers)
        if user_info_response.status_code != 200:
            raise HTTPException(
                status_code=user_info_response.status_code,
                detail=f"Google user info error: {user_info_response.text}",
            )

    user_info = user_info_response.json()
    return JSONResponse(content={"user": user_info, "redirect_url": "/"})
