import re

import logging
from typing import Optional
from pydantic import BaseModel, Field, field_validator

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

    @field_validator('email')
    def validate_email(cls, value):
        if not re.match(email_regex, value):
            logger.error('Invalid email')
            raise ValueError('Invalid email')
        return value


    @field_validator('phone')
    def validate_phone(cls, value):
        if not re.match(phone_regex, value):
            logger.error('Invalid phone')
            raise ValueError('Invalid phone')
        return value


    class Config:
        from_attributes = True
