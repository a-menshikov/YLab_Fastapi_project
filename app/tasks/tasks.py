from celery import Celery

from app.config import REDIS_HOST, REDIS_PORT

# from app.config import (
#     RABBITMQ_DEFAULT_PASS,
#     RABBITMQ_DEFAULT_PORT,
#     RABBITMQ_DEFAULT_USER,
#     RABBITMQ_HOST,
# )
from app.tasks.parser import ParserRepo

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')
# celery = Celery(
#     'tasks',
#     broker=(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@'
#             f'{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}')
# )


@celery.task(default_retry_delay=5, max_retries=None)
def task_test():
    parser = ParserRepo()
    print(parser.parser())
    task_test.retry()
