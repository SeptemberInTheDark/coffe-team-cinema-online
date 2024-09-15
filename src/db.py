#sync
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME
)


DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'



engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(f'SessionLocal: {SessionLocal}')


Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



