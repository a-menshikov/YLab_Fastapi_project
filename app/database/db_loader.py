import os

from aioredis import ConnectionPool, Redis
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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

conn_url = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
            f'@database/{POSTGRES_DB}')
Base = declarative_base()
engine = create_async_engine(conn_url)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                 bind=engine, class_=AsyncSession)


async def get_db():
    """Возвращает соединение с базой данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def init_db():
    """Создание таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_redis():
    """Создание пула соединений с Redis."""
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis():
    """Возвращает соединение с Redis."""
    return Redis(connection_pool=pool)
