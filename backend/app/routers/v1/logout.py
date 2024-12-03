from fastapi import APIRouter, Response


router = APIRouter()


@router.post('')
async def logout(response: Response):
    response.delete_cookie("_key_token")
    return {"status": "success"}
