from sqlalchemy.orm import Session

from app.database.models import Submenu
from app.database.schemas import SubmenuRead, SubmenuPost


def create_submenu(db: Session, submenu: SubmenuPost, menu_id: str):
    """Добавление нового подменю."""
    new_submenu = Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def update_submenu(db: Session, current_submenu: SubmenuRead,
                   updated_submenu: SubmenuPost):
    """Изменение подменю по id."""
    current_submenu.title = updated_submenu.title
    current_submenu.description = updated_submenu.description
    db.merge(current_submenu)
    db.commit()
    db.refresh(current_submenu)
    return current_submenu


def get_submenu_by_title(db: Session, title: str, menu_id: str):
    """Получение подменю по title."""
    return db.query(Submenu).filter(
        Submenu.title == title,
        Submenu.menu_id == menu_id
    ).first()


def get_submenu_by_id(db: Session, id: str):
    """Получение подменю по id."""
    return db.query(Submenu).filter(
        Submenu.id == id,
    ).first()
