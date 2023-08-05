from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.crud_repository import SubmenuRepository
from app.database.db_loader import get_db
from app.database.models import Dish
from app.database.schemas import DishPost
from app.database.services import check_objects, check_unique_dish


class DishRepository:
    """Репозиторий CRUD операций модели блюда."""

    def __init__(self, db: Session = Depends(get_db),
                 submenu_repo: SubmenuRepository = Depends()) -> None:
        self.db = db
        self.submenu_repo = submenu_repo
        self.model = Dish

    def create_dish(self, dish: DishPost, menu_id: str,
                    submenu_id: str) -> Dish:
        """Добавление нового блюда."""
        try:
            check_unique_dish(db=self.db, dish=dish)
        except FlushError:
            raise FlushError('Блюдо с таким названием и описанием уже есть')
        try:
            check_objects(db=self.db, menu_id=menu_id, submenu_id=submenu_id)
        except NoResultFound as error:
            raise NoResultFound(error.args[0])
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
        )
        self.db.add(new_dish)
        self.db.commit()
        self.db.refresh(new_dish)
        return new_dish

    def update_dish(self, dish_id: str, updated_dish: DishPost) -> Dish:
        """Изменение блюда по id."""
        current_dish = self.get_dish_by_id(id=dish_id)
        if not current_dish:
            raise NoResultFound('dish not found')
        try:
            check_unique_dish(db=self.db, dish=updated_dish)
        except FlushError:
            raise FlushError('Блюдо с таким названием и описанием уже есть')
        current_dish.title = updated_dish.title
        current_dish.description = updated_dish.description
        current_dish.price = updated_dish.price
        self.db.merge(current_dish)
        self.db.commit()
        self.db.refresh(current_dish)
        return current_dish

    def get_dish_by_id(self, id: str) -> Dish:
        """Получение блюда по id."""
        dish = self.db.query(Dish).filter(
            Dish.id == id,
        ).first()
        if not dish:
            raise NoResultFound('dish not found')
        return dish

    def get_all_dishes(self, submenu_id: str) -> list[Dish]:
        """Получение всех блюд."""
        try:
            current_submenu = self.submenu_repo.get_submenu_by_id(
                id=submenu_id
            )
        except NoResultFound:
            return []
        return current_submenu.dishes

    def delete_dish(self, dish_id: str) -> None:
        """Удаление блюда по id."""
        current_dish = self.get_dish_by_id(id=dish_id)
        if not current_dish:
            raise NoResultFound('dish not found')
        self.db.delete(current_dish)
        self.db.commit()
