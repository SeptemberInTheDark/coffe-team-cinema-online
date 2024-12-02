from fastapi import APIRouter
from .v1.register import router as reg_router



v1 = APIRouter()

v1.include_router(reg_router, prefix='/register', tags=['регистрация пользователя'])
