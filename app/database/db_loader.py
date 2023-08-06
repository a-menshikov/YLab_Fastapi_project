import os

from dotenv import load_dotenv
from redis import ConnectionPool, Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
EXPIRATION = 3600
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

conn_url = (f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
            f'@database/{POSTGRES_DB}')
engine = create_engine(conn_url)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Возвращает соединение с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_redis():
    """Создание пула соединений с Redis."""
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis():
    """Возвращает соединение с Redis."""
    return Redis(connection_pool=pool)
