from sqlalchemy.orm import Session

from app.database.models import Menu
from app.database.schemas import MenuPost, MenuRead


def create_menu(db: Session, menu: MenuPost):
    """Добавление нового меню."""
    db_menu = Menu(
        title=menu.title,
        description=menu.description,
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, current_menu: MenuRead, updated_menu: MenuPost):
    """Изменение меню по id."""
    current_menu.title = updated_menu.title
    current_menu.description = updated_menu.description
    db.merge(current_menu)
    db.commit()
    db.refresh(current_menu)
    return current_menu


def get_menu_by_title(db: Session, title: str):
    """Получение меню по title."""
    return db.query(Menu).filter(Menu.title == title).first()


def get_menu_by_id(db: Session, id: str):
    """Получение меню по id."""
    return db.query(Menu).filter(Menu.id == id).first()


def get_all_menus(db: Session):
    """Получение всех меню."""
    return db.query(Menu).all()
