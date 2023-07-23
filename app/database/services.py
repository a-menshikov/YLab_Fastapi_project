from typing import Optional

from sqlalchemy import exists
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.database.models import Dish, Menu, Submenu


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
