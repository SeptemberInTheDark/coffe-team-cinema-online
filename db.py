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

"""
Альтернативное создание базового класса
from sqlalchemy import MetaData, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase,


class BaseModel(DeclarativeBase):
    metadata = MetaData()
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
В дальнейшем при создании моделей наследуемся от базового класса
тк он уже содержит метаданные, то прописывать 
Base.metadata.create_all(bind=engine) уже не требуется та-же в него можно поместить поля 
моделей по умолчанию например created_at.
"""


async def get_session() -> Session:
    with SessionLocal() as session:
        yield session