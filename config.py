from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """
        Database settings
        """
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file: str = ".env"


settings = Settings()
