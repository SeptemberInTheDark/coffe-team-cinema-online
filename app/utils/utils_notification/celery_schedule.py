from jinja2 import Template

from celery import Celery
from celery.schedules import crontab

from email.mime.text import MIMEText

from app.utils.utils_notification.mail_service import send_email
from app.core.config import settings
from app.core.init_db import AsyncSessionFactory
from app.crud.crud_user import NotificationCRUD
from app.crud.crud_movies import MovesCRUD
from app.crud.crud_category import CategoryCRUD
from app.utils.logging import AppLogger
import asyncio


logger = AppLogger().get_logger()


celery_app = Celery("email_sending", broker=settings.REDIS_URL)
celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "sending-mails": {
            "task": "send_email",
            "schedule": crontab(
                day_of_week=settings.DAY_OF_WEEK, hour=settings.HOUR, minute=settings.MINUTE
            ),  # TODO переместить время в конфиг
        },
    },
)

async def proposal_creation():
    session = AsyncSessionFactory()
    all_category = await CategoryCRUD.get_all_categories(session)
    proposals = {}

    for category in all_category:
        proposals[category.name] = await MovesCRUD.search_movies_by_category(session=session, category_id=category.id, limit=3)

    logger.info("Proposals created: %s", proposals)

    return proposals


@celery_app.task(name="send_email")
def send_notifications():
    db = AsyncSessionFactory()

    # Получение уведомлений с помощью асинхронного запроса
    async def get_notifications_async():
        return await NotificationCRUD.get_notifications(db)

    loop = asyncio.get_event_loop()
    all_notifications = loop.run_until_complete(get_notifications_async())


    loop = asyncio.get_event_loop()
    all_movies = loop.run_until_complete(proposal_creation())

    # Проверка наличия уведомлений
    if not all_notifications:
        logger.info("No notifications to send")
        return
    
    # Загрузка HTML-шаблона
    with open("app/utils/utils_notification/email_template.html", "r") as file:
            html_text = file.read()
    email_template = Template(html_text)

    # Отправка уведомлений
    for tuple_notification in all_notifications:
        notification = tuple_notification[0]

        print("all_movies", all_movies)
        # Рендеринг HTML-шаблона для конкретного пользователя
        html_content = email_template.render(
            username=notification.email,
            suggestions=all_movies,
        )
        html_message = MIMEText(
            html_content, "html", "utf-8"
        )

        # Отправка уведомления
        send_email("test_subject", html_message, notification.email)
        logger.info(f"Email sent to {notification.email}")
    return all_movies


# Запуск Celery
# python -m celery -A app.utils.utils_notification.celery_schedule.celery_app worker --loglevel=info
# python -m celery -A app.utils.utils_notification.celery_schedule.celery_app beat --loglevel INFO
