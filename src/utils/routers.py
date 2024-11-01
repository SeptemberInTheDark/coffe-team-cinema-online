from src.Users.reset_pass.reset_pass_handlers import reset_pass_router
from src.register.router import router as register_router
from src.Users.router import router as user_router
from src.auth.router import router as auth_router
from src.auth.logout.router import router as logout_router


def register_routers(app):
    app.include_router(register_router)
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(reset_pass_router)
    app.include_router(logout_router)
