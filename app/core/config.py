from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    ALGORITHM: str = 'HS256'
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    REDIS_URL: str

    SMTP_PASS: str
    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PORT: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    PHONE_VALIDATOR: str
    EMAIL_VALIDATOR: str

    DATABASE_URL_TEST: str

    REDIS_URL: str

    #FastAPI
    FASTAPI_API_V1_PATH: str = '/api/v1'
    FASTAPI_TITLE: str = 'Your Online Cinema'
    FASTAPI_DESCRIPTION: str = 'Онлайн кинотеатр(бэкенд)'
    FASTAPI_DOCS_URL: str | None = f'{FASTAPI_API_V1_PATH}/docs'
    FASTAPI_OPENAPI_URL: str | None = f'{FASTAPI_API_V1_PATH}/openapi'
    FASTAPI_STATIC_FILES: bool = True

    #Middleware
    MIDDLEWARE_CORS: bool = True

    #Trace ID
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'

    # GOOGLE_CLIENT_ID: str
    # GOOGLE_CLIENT_SECRET: str
    # GOOGLE_REDIRECT_URI: str
    #
    # YANDEX_CLIENT_ID: str
    # YANDEX_CLIENT_SECRET: str
    # YANDEX_REDIRECT_URI: str
    #
    # MAILRU_CLIENT_ID: str
    # MAILRU_CLIENT_SECRET: str
    # MAILRU_REDIRECT_URI: str

    #CORS
    CORS_ALLOWED_ORIGINS: list[str] = [
        'http://127.0.0.1:8000',
        'http://localhost:5173',
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        TRACE_ID_REQUEST_HEADER_KEY
    ]


    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
