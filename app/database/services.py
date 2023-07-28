from typing import Optional

from app.database.models import Dish, Menu, Submenu
from app.database.schemas import DishPost, MenuPost, SubmenuPost
from sqlalchemy import exists
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound


def check_objects(db: Session, menu_id: Optional[str] = None,
                  submenu_id: Optional[str] = None,
                  dish_id: Optional[str] = None):
    """Проверка на существование объектов"""
    if menu_id:
        if not db.query(exists().where(Menu.id == menu_id)).scalar():
            raise NoResultFound("menu not found")

    if submenu_id:
        if not db.query(exists().where(Submenu.id == submenu_id)).scalar():
            raise NoResultFound("submenu not found")

    if dish_id:
        if not db.query(exists().where(Dish.id == dish_id)).scalar():
            raise NoResultFound("dish not found")


def check_unique_dish(db: Session, dish: DishPost):
    """Проверка на существование блюда."""
    if db.query(exists().where(Dish.title == dish.title,
                               Dish.description == dish.description)).scalar():
        raise FlushError


def check_unique_menu(db: Session, menu: MenuPost):
    """Проверка на существование меню."""
    if db.query(exists().where(Menu.title == menu.title)).scalar():
        raise FlushError


def check_unique_submenu(db: Session, submenu: SubmenuPost):
    """Проверка на существование подменю."""
    if db.query(exists().where(Submenu.title == submenu.title)).scalar():
        raise FlushError
