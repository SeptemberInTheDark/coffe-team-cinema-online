from fastapi import FastAPI
from sqladmin import Admin

from .init_db import engine
from .path_settings import STATIC_DIR
from .config import settings
from app.router import route
from ..admin.views import UserAdmin, MovieAdmin, ActorAdmin, NewsAdmin


# @asynccontextmanager
# async def register_init(app: FastAPI):
#     yield create_db_and_tables()


def register_app():
    #FastAPI

    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
    )

    register_middleware(app)
    register_static_file(app)
    register_router(app)
    register_admin(app, engine)



    return app

def register_admin(app: FastAPI, engine):
    admin = Admin(app, engine, base_url="/api/v1/admin", title="Админка")
    admin.add_view(UserAdmin)
    admin.add_view(MovieAdmin)
    admin.add_view(ActorAdmin)
    admin.add_view(NewsAdmin)
    return admin

def register_static_file(app: FastAPI):
    if settings.FASTAPI_STATIC_FILES:
        from fastapi.staticfiles import StaticFiles
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


def register_router(app: FastAPI):
    #API
    app.include_router(route)
