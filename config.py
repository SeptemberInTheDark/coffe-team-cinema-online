from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Основные настройки
    ALGORITHM: str
    SECRET_KEY: str

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

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    SMTP_PASS: str
    SMTP_USER: str
    SMTP_PORT: int
    SMTP_HOST: str

    # Yandex OAuth
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str

    # VK OAuth
    VK_CLIENT_ID: str
    VK_CLIENT_SECRET: str
    VK_REDIRECT_URI: str

    # Префикс для API OAuth маршрутов
    API_OAuth_PREFIX: str = "/api/oauth/v1"

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


settings = Settings()
