import logging

from celery import Celery

from app.config import (
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
)
from app.tasks.parser import ParserRepo
from app.tasks.updater import BaseUpdaterRepo

celery = Celery(
    'tasks',
    broker=(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@'
            f'{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}')
)


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_base():
    """Задача обновления данных в базе из файла."""
    try:
        parser = ParserRepo()
        parser_data = parser.parser()
        updater = BaseUpdaterRepo(parser_data)
        updater.run()
    except Exception as error:
        # сложно заложить обработку всех кейсов, которые пользователь
        # может навертеть в файле, поэтому ловим всё и смотрим
        # что не так уже в логах. задача должна повторяться даже после ошибки.
        logging.error(error)
    finally:
        update_base.retry()
