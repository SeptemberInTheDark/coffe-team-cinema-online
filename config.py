from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

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

    REDIS_URL: str


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
