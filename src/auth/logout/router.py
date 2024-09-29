from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/api/logout',
    tags=['Авторизация пользователя']
)

@router.post('')
async def logout():
    pass
