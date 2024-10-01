from fastapi import APIRouter, Response


router = APIRouter(
    prefix='/api/logout',
    tags=['Выход с аккаунта']
)


@router.post('')
async def logout(response: Response):
    response.delete_cookie("_key_token")
    return {"status": "success"}
