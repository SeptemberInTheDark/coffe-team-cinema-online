import re
import secrets
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException

from config import settings
from src.utils.logging import AppLogger

email_regex = settings.EMAIL_VALIDATOR
phone_regex = settings.PHONE_VALIDATOR

logger = AppLogger().get_logger()


def get_email_template(user: str,
                       email_address: str,
                       reset_code: str):
    email = EmailMessage()
    email["Subject"] = f"Сброс пароля для аккаунта {user}"
    email["From"] = settings.SMTP_USER
    email["To"] = email_address

    email.set_content(
        '<div>'
        f'<h1>Сброс пароля для аккаунта {user}</h1>'
        f'<p>Ваш код для сброса пароля: {reset_code}</p>'
        '</div>',
        subtype="html"
    )
    return email


def send_email_reset_code(email: str,
                          reset_code: str,
                          user_name: str):
    try:
        email = get_email_template(user=user_name,
                                   email_address=email,
                                   reset_code=reset_code)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
            smtp.send_message(email)
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error("Ошибка при отправке сообщения на %s\nошибка: %e", email, e)
        raise HTTPException(status_code=500, detail="Ошибка при отправке сообщения")


def generate_reset_code():
    """
    Функция генерирует код для сброса пароля
    """
    return secrets.token_hex(4)


def is_valid_email(email: str) -> bool:
    return re.fullmatch(email_regex, email) is not None


def is_valid_phone(phone: str) -> bool:
    return re.fullmatch(phone_regex, phone) is not None
