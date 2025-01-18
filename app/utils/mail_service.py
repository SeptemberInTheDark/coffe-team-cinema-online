import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


def get_server(mail_host: str, mail_port: int):
    return smtplib.SMTP_SSL(
        host=mail_host,
        port=mail_port
    )


def send_email(subject: str, content: str, receiver: str):
    server = get_server(settings.SMTP_HOST, settings.SMTP_PORT)
    try:
        sender = settings.SMTP_USER
        password = settings.SMTP_PASS

        mail = EmailMessage()
        mail.add_header("subject", subject)
        mail.add_header("from", sender)
        mail.add_header("to", receiver)
        mail.set_content(content)
        

        server.login(sender, password)
        server.send_message(mail)
        server.send

    except smtplib.SMTPAuthenticationError as e:
        logger.error("Ошибка при логинировании %s", e)
        return "Неправильное имя пользователя или пароль"
