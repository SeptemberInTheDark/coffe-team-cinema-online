from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/api',
    tags=['Личный кабинет'],
)

@router.get('/me')
async def my_account(db: AsyncSession = Depends(get_db)):
    pass
