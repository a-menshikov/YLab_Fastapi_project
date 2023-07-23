from sqlalchemy.orm import Session

from app.database.models import Dish
from app.database.schemas import DishRead, DishPost


def create_dish(db: Session, dish: DishPost, submenu_id: str):
    """Добавление нового блюда."""
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


def update_dish(db: Session, current_dish: DishRead, updated_dish: DishPost):
    """Изменение блюда по id."""
    current_dish.title = updated_dish.title
    current_dish.description = updated_dish.description
    current_dish.price = updated_dish.price
    db.merge(current_dish)
    db.commit()
    db.refresh(current_dish)
    return current_dish


def get_dish_by_id(db: Session, id: str, submenu_id: str):
    """Получение блюда по id."""
    return db.query(Dish).filter(
        Dish.id == id,
        Dish.submenu_id == submenu_id,
    ).first()
