import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import select, func

from app.database.db_loader import Base


class Dish(Base):
    """Модель блюда."""

    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(precision=10, scale=2, decimal_return_scale=2),
                   nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates="dishes")


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
