from celery import Celery
from celery.schedules import crontab

from app.utils.mail_service import send_email
from app.core.config import settings
from app.core.init_db import AsyncSessionFactory
from app.crud.crud_user import NotificationCRUD
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


@celery_app.task(name="send_email")
def send_notifications():
    db = AsyncSessionFactory()

    async def get_notifications_async():
        return await NotificationCRUD.get_notifications(db)

    loop = asyncio.get_event_loop()
    all_notifications = loop.run_until_complete(get_notifications_async())

    if not all_notifications:
        logger.info("No notifications to send")
        return

    for tuple_notification in all_notifications:
        notification = tuple_notification[0]
        send_email("test_subject", "test_message", notification.email)
        logger.info(f"Email sent to {notification.email}")
    return


# Запуск Celery
# python -m celery -A app.utils.celery_schedule.celery_app worker --loglevel=info
# python -m celery -A app.utils.celery_schedule.celery_app beat --loglevel INFO
