import datetime


from celery import Celery
from celery.schedules import crontab
from app.utils.mail_service import send_email
from app.core.config import settings

celery_app = Celery('email_sending', broker=settings.REDIS_URL)
celery_app.conf.update(
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'sending-mails': {
            'task': 'send_email',
            'schedule': crontab(day_of_week="sunday",  hour="18", minute="00"), # TODO переместить время в конфиг
        },
    },
)

@celery_app.task(name='send_email')
def say_time():
    # send_email("test_subject", "test_message", "test_email")
    print(datetime.datetime.now())


# Запуск Celery
# python -m celery -A app.utils.celery_schedule.celery_app worker --loglevel=info
# python -m celery -A app.utils.celery_schedule.celery_app beat --loglevel INFO
