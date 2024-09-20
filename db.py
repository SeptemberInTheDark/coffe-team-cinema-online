# sync
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from config import settings

DATABASE_URL = (f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@'
                f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(f'SessionLocal: {SessionLocal}')

Base = declarative_base()

Base.metadata.create_all(bind=engine)


async def get_session() -> Session:
    with SessionLocal() as session:
        yield session