from fastapi import Depends

from app.api.dishes.crud_repository import DishRepository
from app.database.cache_repository import СacheRepository
from app.database.models import Dish
from app.database.schemas import DishPost


class DishService:
    """Сервисный репозиторий для блюд."""

    def __init__(self, crud_repo: DishRepository = Depends(),
                 cache_repo: СacheRepository = Depends()) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_dishes(self, submenu_id: str,
                             menu_id: str) -> list[Dish]:
        """Получение всех блюд."""
        cache = await self.cache_repo.get_all_dishes_cache(menu_id, submenu_id)
        if cache:
            return cache
        items = await self.crud_repo.get_all_dishes(submenu_id=submenu_id)
        await self.cache_repo.set_all_dishes_cache(menu_id, submenu_id, items)
        return items

    async def get_dish_by_id(self, id: str, menu_id: str,
                             submenu_id: str) -> Dish:
        """Получение блюда по id."""
        cache = await self.cache_repo.get_dish_cache(id, menu_id, submenu_id)
        if cache:
            return cache
        item = await self.crud_repo.get_dish_by_id(id=id)
        await self.cache_repo.set_dish_cache(item, submenu_id, menu_id)
        return item

    async def create_dish(self, dish: DishPost, menu_id: str,
                          submenu_id: str) -> Dish:
        """Добавление нового блюда."""
        item = await self.crud_repo.create_dish(dish=dish, menu_id=menu_id,
                                                submenu_id=submenu_id)
        await self.cache_repo.create_dish_cache(item, submenu_id, menu_id)
        return item

    async def update_dish(self, dish_id: str, submenu_id: str, menu_id: str,
                          updated_dish: DishPost) -> Dish:
        """Изменение блюда по id."""
        item = await self.crud_repo.update_dish(dish_id=dish_id,
                                                updated_dish=updated_dish)
        await self.cache_repo.update_dish_cache(item, submenu_id=submenu_id,
                                                menu_id=menu_id)
        return item

    async def delete_dish(self, dish_id: str, submenu_id: str,
                          menu_id: str) -> None:
        """Удаление блюда по id."""
        await self.cache_repo.delete_dish_cache(dish_id, submenu_id, menu_id)
        await self.crud_repo.delete_dish(dish_id=dish_id)
