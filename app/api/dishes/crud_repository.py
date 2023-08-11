from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.crud_repository import SubmenuRepository
from app.database.db_loader import get_db
from app.database.models import Dish
from app.database.schemas import DishPost
from app.database.services import check_objects, check_unique_dish


class DishRepository:
    """Репозиторий CRUD операций модели блюда."""

    def __init__(self, db: AsyncSession = Depends(get_db),
                 submenu_repo: SubmenuRepository = Depends()) -> None:
        self.db = db
        self.submenu_repo = submenu_repo
        self.model = Dish

    async def create_dish(self, dish: DishPost, menu_id: str,
                          submenu_id: str) -> Dish:
        """Добавление нового блюда."""
        try:
            await check_unique_dish(db=self.db, dish=dish)
        except FlushError:
            raise FlushError('Блюдо с таким названием и описанием уже есть')
        try:
            await check_objects(db=self.db, menu_id=menu_id,
                                submenu_id=submenu_id)
        except NoResultFound as error:
            raise NoResultFound(error.args[0])
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
        )
        self.db.add(new_dish)
        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def update_dish(self, dish_id: str, updated_dish: DishPost) -> Dish:
        """Изменение блюда по id."""
        current_dish = await self.get_dish_by_id(id=dish_id)
        if not current_dish:
            raise NoResultFound('dish not found')
        try:
            await check_unique_dish(db=self.db, dish=updated_dish)
        except FlushError:
            raise FlushError('Блюдо с таким названием и описанием уже есть')
        current_dish.title = updated_dish.title
        current_dish.description = updated_dish.description
        current_dish.price = updated_dish.price
        await self.db.merge(current_dish)
        await self.db.commit()
        await self.db.refresh(current_dish)
        return current_dish

    async def get_dish_by_id(self, id: str) -> Dish:
        """Получение блюда по id."""
        dish = (await self.db.execute(
            select(self.model).where(self.model.id == id)
        )).scalar()
        if not dish:
            raise NoResultFound('dish not found')
        return dish

    async def get_all_dishes(self, submenu_id: str) -> list[Dish]:
        """Получение всех блюд."""
        try:
            await check_objects(db=self.db, submenu_id=submenu_id)
        except NoResultFound:
            return []
        return ((await self.db.execute(
            select(self.model).where(self.model.submenu_id == submenu_id)
        )).scalars().all())

    async def delete_dish(self, dish_id: str) -> None:
        """Удаление блюда по id."""
        current_dish = await self.get_dish_by_id(id=dish_id)
        if not current_dish:
            raise NoResultFound('dish not found')
        await self.db.delete(current_dish)
        await self.db.commit()
