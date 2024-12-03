from fastapi import APIRouter
from .v1.register import router as reg_router
from .v1.auth import router as auth_router
from .v1.logout import router as logout_router
from .v1.user import router as user_router
from .v1.auth_services import router as oauth_router

v1 = APIRouter()

v1.include_router(reg_router, prefix='/register', tags=['регистрация пользователя'])
v1.include_router(auth_router, prefix='/login', tags=['Авторизация пользователя'])
v1.include_router(logout_router, prefix='/logout', tags=['Выход с аккаунта'])
v1.include_router(user_router, prefix='/users/', tags=['Получение пользотеля/пользователей'])
v1.include_router(oauth_router)
