import logging
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from config import settings

"""
Регулярное выражение для телефона: (?:\+7|7|8)[-\s\(]?(\d{3})[\)\s-]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})
Регулярное выражение для почты: (^[\w\.-]+@[\w\.-]+\.\w{2,}$)
"""

email_regex = settings.EMAIL_VALIDATOR
phone_regex = settings.PHONE_VALIDATOR

logger = logging.getLogger(__name__)


class User(BaseModel):
    id: int | None = None
    username: str
    email: str
    phone: str
    hashed_password: str
    is_active: Optional[bool] = True


class UserCreate(User):
    username: str
    hashed_password: str
    phone: str
    email: str

    model_config = ConfigDict(from_attributes=True)



class PasswordResetConfirm(BaseModel):
    """
    Модель для подтверждения кода и сброса пароля
    """
    email: EmailStr
    reset_code: str
    new_password: str
