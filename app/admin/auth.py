#from fastapi import Depends
#from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
#from starlette.responses import RedirectResponse

from app.controllers.jwt_controller import JWTManager
from app.routers.v1.auth import auth_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        # аутентификация пользователя
        user = await auth_user(username,password)
        if user:
            access_token = JWTManager.encode_jwt({"sub": username})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")

