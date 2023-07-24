import uuid

from app.database.db_loader import Base
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import func, select


class Dish(Base):
    """Модель блюда."""

    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # очень странно хранить цену в строке, но тесты ждут в ответ строку
    # пока мы с ценой никаких операций не производим и обратная конвертация
    # нигде не требуется оставил строку с предобработкой в схеме
    price = Column(String(20), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates="dishes")

    # выбран UniqueConstraint этих полей, потому что в подменю могут быть
    # одинаковые блюда, но с разным описанием - порции, на вынос или в зале
    # и так далее
    __table_args__ = (
        UniqueConstraint('title', 'description',
                         name='uq_title_description'),
    )


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
    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id == id).correlate_except(Dish).as_scalar()
    )


class Menu(Base):
    """Модель меню."""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    submenus = relationship('Submenu', back_populates="menu",
                            cascade='all, delete')
    submenus_count = column_property(
        select(func.count(Submenu.id)).where(
            Submenu.menu_id == id).correlate_except(Submenu).as_scalar()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(Submenu.id).where(Submenu.menu_id == id)
        )).correlate_except(Dish).as_scalar()
    )
