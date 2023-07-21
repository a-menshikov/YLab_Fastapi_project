from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

conn_url = 'postgresql+psycopg2://artem:ahea31ahea31@database/menu_db'
engine = create_engine(conn_url)
Base = declarative_base()
