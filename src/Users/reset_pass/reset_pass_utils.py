import re
import secrets

from fastapi import HTTPException

from config import settings
from src.utils.logging import AppLogger

email_regex = settings.EMAIL_VALIDATOR
phone_regex = settings.PHONE_VALIDATOR

logger = AppLogger().get_logger()


# Функция для отправки email
def send_email(email: str, reset_code: str):
    try:
        pass
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")


def generate_reset_code():
    """
    Функция генерирует код для сброса пароля
    """
    return secrets.token_hex(4)


def is_valid_email(email: str) -> bool:
    return re.fullmatch(email_regex, email) is not None


def is_valid_phone(phone: str) -> bool:
    return re.fullmatch(phone_regex, phone) is not None
