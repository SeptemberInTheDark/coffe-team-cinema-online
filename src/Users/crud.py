from sqlalchemy.orm import Session
from . import models, schemas
from .manager import UserHashManager
import os


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_user_by_login(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session):
    return db.query(models.User).offset(skip).limit(limit).all()


def check_user(db: Session, username: str, email: str, phone: str):
    try:
        existing_user = db.query(models.User).filter(
            (models.User.username == username) |
            (models.User.email == email) |
            (models.User.phone == phone)
        ).first()
        return existing_user if existing_user else None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None


def create_user(db: Session, user: schemas.UserCreate):
    user_salt = os.urandom(32).hex()
    hashed_password = UserHashManager.hash_str(user.hashed_password, user_salt)

    db_user = models.User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    user = db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return True

    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return False

#На потом
def update_user_info():
    pass
