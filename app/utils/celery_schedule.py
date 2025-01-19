import datetime

from celery import Celery
from celery.schedules import crontab
from app.utils.mail_service import send_email

celery_app = Celery('email_sending', broker='redis://0.0.0.0:6379/0') # TODO вынести в конфиг
celery_app.conf.update(
    timezone='UTC',  # Укажите нужный вам часовой пояс, например, 'Europe/Moscow'
    enable_utc=True,
    beat_schedule={  # Добавляем расписание задач
        'sending-mails': {
            'task': 'send_email',
            'schedule': crontab(minute='*/1'), # TODO заменить время на необходимое
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
