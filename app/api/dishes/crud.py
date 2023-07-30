from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.crud import get_submenu_by_id
from app.database.models import Dish
from app.database.schemas import DishPost
from app.database.services import check_objects, check_unique_dish


def create_dish(db: Session, dish: DishPost, menu_id: str, submenu_id: str):
    """Добавление нового блюда."""
    try:
        check_unique_dish(db=db, dish=dish)
    except FlushError:
        raise FlushError("Блюдо с таким названием и описанием уже есть")
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise NoResultFound(error.args[0])
    new_dish = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


def update_dish(db: Session, dish_id: str, updated_dish: DishPost):
    """Изменение блюда по id."""
    current_dish = get_dish_by_id(db=db, id=dish_id)
    if not current_dish:
        raise NoResultFound("dish not found")
    try:
        check_unique_dish(db=db, dish=updated_dish)
    except FlushError:
        raise FlushError("Блюдо с таким названием и описанием уже есть")
    current_dish.title = updated_dish.title
    current_dish.description = updated_dish.description
    current_dish.price = updated_dish.price
    db.merge(current_dish)
    db.commit()
    db.refresh(current_dish)
    return current_dish


def get_dish_by_id(db: Session, id: str):
    """Получение блюда по id."""
    dish = db.query(Dish).filter(
        Dish.id == id,
    ).first()
    if not dish:
        raise NoResultFound("dish not found")
    return dish


def get_all_dishes(db: Session, submenu_id: str):
    """Получение всех блюд."""
    try:
        current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    except NoResultFound:
        return []
    return current_submenu.dishes


def delete_dish(db: Session, dish_id: str):
    """Удаление блюда по id."""
    current_dish = get_dish_by_id(db=db, id=dish_id)
    if not current_dish:
        raise NoResultFound("dish not found")
    db.delete(current_dish)
    db.commit()
