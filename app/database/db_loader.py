from aioredis import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import REDIS_URL, conn_url

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
