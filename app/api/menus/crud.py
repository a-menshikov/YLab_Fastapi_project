from sqlalchemy.orm import Session

from app.database.models import Menu
from app.database.schemas import MenuPost


def create_menu(db: Session, menu: MenuPost):
    """Добавление нового меню."""
    db_menu = Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menu_by_title(db: Session, title: str):
    """Получение меню по title."""
    return db.query(Menu).filter(Menu.title == title).first()


def get_menu_by_id(db: Session, id: str):
    """Получение меню по id."""
    return db.query(Menu).filter(Menu.id == id).first()


def get_all_menus(db: Session):
    """Получение всех меню."""
    return db.query(Menu).all()
