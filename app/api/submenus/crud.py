from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.crud import get_menu_by_id
from app.database.models import Submenu
from app.database.schemas import SubmenuPost
from app.database.services import check_objects, check_unique_submenu


def create_submenu(db: Session, submenu: SubmenuPost, menu_id: str):
    """Добавление нового подменю."""
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound as error:
        raise NoResultFound(error.args[0])
    try:
        check_unique_submenu(db=db, submenu=submenu)
    except FlushError:
        raise FlushError("Подменю с таким названием уже есть")
    new_submenu = Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def update_submenu(db: Session, menu_id: str, submenu_id: str,
                   updated_submenu: SubmenuPost):
    """Изменение подменю по id."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise NoResultFound(error.args[0])
    try:
        check_unique_submenu(db=db, submenu=updated_submenu)
    except FlushError:
        raise FlushError("Подменю с таким названием уже есть")
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    current_submenu.title = updated_submenu.title
    current_submenu.description = updated_submenu.description
    db.merge(current_submenu)
    db.commit()
    db.refresh(current_submenu)
    return current_submenu


def get_submenu_by_id(db: Session, id: str):
    """Получение подменю по id."""
    try:
        check_objects(db=db, submenu_id=id)
    except NoResultFound:
        raise NoResultFound("submenu not found")
    return db.query(Submenu).filter(
        Submenu.id == id,
    ).first()


def get_all_submenus(db: Session, menu_id: str):
    """Получение всех подменю."""
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound:
        return []
    else:
        current_menu = get_menu_by_id(db=db, id=menu_id)
        return current_menu.submenus


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    """Удаление подменю конкретного меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise NoResultFound(error.args[0])
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    db.delete(current_submenu)
    db.commit()
