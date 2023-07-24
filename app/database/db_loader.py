import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

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
