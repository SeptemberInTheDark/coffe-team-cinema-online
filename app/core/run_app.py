from fastapi import FastAPI

from .path_settings import STATIC_DIR
from .config import settings
from app.router import route

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

    return app

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
