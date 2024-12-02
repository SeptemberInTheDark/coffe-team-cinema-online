from pydantic import BaseModel, Field, field_validator, EmailStr
import re
from app.core.config import settings
import logging
from typing import Optional



email_regex = settings.EMAIL_VALIDATOR
phone_regex = settings.PHONE_VALIDATOR

logger = logging.getLogger(__name__)


class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    email: str = Field(...)
    phone: str = Field(...)


    @field_validator('email')
    def validate_username(cls, value):
        if not re.fullmatch(email_regex, value):
            raise ValueError("Email должен содержать символ '@' ")
        return value


    @field_validator('phone')
    def validate_username(cls, value):
        if not re.fullmatch(phone_regex, value):
            raise ValueError("Телефон должен начинаться с '+7' ")
        return value




class User(BaseModel):
    id: int | None = None
    username: str
    email: str
    phone: str
    hashed_password: str
    is_active: Optional[bool] = True



class PasswordResetConfirm(BaseModel):
    """
    Модель для подтверждения кода и сброса пароля
    """
    email: EmailStr
    reset_code: str
    new_password: str
