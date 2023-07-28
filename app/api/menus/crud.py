from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.database.models import Menu
from app.database.schemas import MenuPost
from app.database.services import check_objects, check_unique_menu


def get_menu_by_id(db: Session, id: str):
    """Получение меню по id."""
    try:
        check_objects(db=db, menu_id=id)
    except NoResultFound:
        raise NoResultFound("menu not found")
    return db.query(Menu).filter(Menu.id == id).first()


def get_all_menus(db: Session):
    """Получение всех меню."""
    return db.query(Menu).all()


def create_menu(db: Session, menu: MenuPost):
    """Добавление нового меню."""
    try:
        check_unique_menu(db=db, menu=menu)
    except FlushError:
        raise FlushError("Меню с таким названием уже есть")
    db_menu = Menu(
        title=menu.title,
        description=menu.description,
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu_id: str, updated_menu: MenuPost):
    """Изменение меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound:
        raise NoResultFound("menu not found")
    current_menu = get_menu_by_id(db=db, id=menu_id)
    current_menu.title = updated_menu.title
    current_menu.description = updated_menu.description
    db.merge(current_menu)
    db.commit()
    db.refresh(current_menu)
    return current_menu


def delete_menu(db: Session, menu_id: str):
    """Удаление меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound:
        raise NoResultFound("menu not found")
    current_menu = get_menu_by_id(db=db, id=menu_id)
    db.delete(current_menu)
    db.commit()
