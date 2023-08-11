from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import conn_url

test_engine = create_async_engine(conn_url)

TestAsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                     bind=test_engine, class_=AsyncSession)

pytest_plugins = 'tests.fixtures'


async def override_db():
    """Возвращает соединение с базой данных."""
    async with TestAsyncSessionLocal() as async_session:
        yield async_session
