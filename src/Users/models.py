from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, func
from db import Base, engine


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True, index=True)
    phone = Column(String(length=15), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    registered_data = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(bind=engine)
