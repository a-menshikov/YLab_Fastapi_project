from app.database.db_loader import Base
from sqlalchemy import Column, Integer, String, Text


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
