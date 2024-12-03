from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict, validator
import re
from backend.app.core.config import settings
import logging
from typing import Optional

email_regex = settings.EMAIL_VALIDATOR
phone_regex = settings.PHONE_VALIDATOR

logger = logging.getLogger(__name__)


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    phone: str = Field(..., pattern=r'(?:\+7|7|8)[-\s\(]?(\d{3})[\)\s-]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})',
                       description="Номер телефона")
    is_active: Optional[bool] = Field(default=True, description="Активен ли пользователь")

    # id: int | None = None
    # hashed_password: str

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

    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: str = Field(..., min_length=8, description="Пароль пользователя")


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50, description="Имя")
    last_name: Optional[str] = Field(None, max_length=50, description="Фамилия")
    gender: Optional[str] = Field(
        None,
        pattern="^(male|female|other)$",
        description="Пол(male,female,other)"
    )
    country: Optional[str] = Field(None, max_length=100, description="Страна")
    favorite_genre: Optional[str] = Field(None, max_length=50, description="Любимый жанр")

    @validator("first_name", "last_name", "country", "favorite_genre")
    def check_non_empty(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Поле не может быть пустой строкой.")
        return value


class PasswordResetConfirm(BaseModel):
    """
    Модель для подтверждения кода и сброса пароля
    """
    email: EmailStr = Field(..., description="Электроннаяпочта")
    reset_code: str = Field(..., min_length=6, max_length=6, description="Код сброса пароля")
    new_password: str = Field(..., min_length=8, description="Новый пароль")
