from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from db import Base


class User(Base):
    __tablename__ = "users_test"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=25), nullable=False)

    firts_name = Column(String(length=25), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False)
    phone = Column(String(length=15), nullable=False)



def get_users(db: Session):
    users = db.query(User).all()
    print(users)
    return users
