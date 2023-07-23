import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db_loader import Base


class Menu(Base):
    """Модель меню."""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    submenus = relationship('Submenu', back_populates="menu",
                            cascade='all, delete')


class Submenu(Base):
    """Модель подменю."""

    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    dishes = relationship('Dish', back_populates="submenu",
                          cascade='all, delete')
    menu = relationship('Menu', back_populates="submenus")


class Dish(Base):
    """Модель блюда."""

    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(scale=2), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates="dishes")
