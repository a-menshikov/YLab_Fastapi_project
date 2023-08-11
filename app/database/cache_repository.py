import pickle

from aioredis import Redis
from fastapi import Depends

from app.api.dishes.crud_repository import DishRepository
from app.api.menus.crud_repository import MenuRepository
from app.api.submenus.crud_repository import SubmenuRepository
from app.database.db_loader import EXPIRATION, get_redis
from app.database.models import Dish, Menu, Submenu


class СacheRepository():
    """Сервисный репозиторий для кеширования объектов."""

    def __init__(self, menu_repo: MenuRepository = Depends(),
                 submenu_repo: SubmenuRepository = Depends(),
                 dish_repo: DishRepository = Depends(),
                 cacher: Redis = Depends(get_redis)) -> None:
        self.cacher = cacher
        self.menu_repo = menu_repo
        self.submenu_repo = submenu_repo
        self.dish_repo = dish_repo

    async def set_all_dishes_cache(self, submenu_id: str,
                                   items: list[Dish]) -> None:
        """Запись всех блюд в кеш."""
        await self.cacher.set(f'all_dishes_{submenu_id}',
                              pickle.dumps(items), ex=EXPIRATION)

    async def get_all_dishes_cache(self, submenu_id: str) -> list[Dish] | None:
        """Получение всех блюд из кеша."""
        cache = await self.cacher.get(f'all_dishes_{submenu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_dish_cache(self, item: Dish) -> None:
        """Запись блюда в кеш."""
        await self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    async def get_dish_cache(self, id: str) -> Dish | None:
        """Получение блюда из кеша."""
        cache = await self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def delete_related_dish_cache(self, submenu_id: str,
                                        menu_id: str) -> None:
        """Удаление кэша связанных с блюдом объектов."""
        await self.delete_all_dish_cache(submenu_id)
        await self.cacher.delete(submenu_id)
        await self.delete_all_submenu_cache(menu_id)
        await self.cacher.delete(menu_id)
        await self.delete_all_menu_cache()

    async def create_dish_cache(self, item: Dish, submenu_id: str,
                                menu_id: str) -> None:
        """Работа с кэшем при создании нового блюда."""
        await self.delete_related_dish_cache(submenu_id, menu_id)
        await self.set_dish_cache(item)

    async def update_dish_cache(self, item: Dish) -> None:
        """Работа с кэшем при изменении блюда."""
        await self.delete_all_dish_cache(str(item.submenu_id))
        await self.set_dish_cache(item)

    async def delete_dish_cache(self, dish_id: str, submenu_id: str,
                                menu_id: str) -> None:
        """Работа с кэшем при удалении блюда."""
        await self.cacher.delete(dish_id)
        await self.delete_related_dish_cache(submenu_id, menu_id)

    async def delete_all_dish_cache(self, submenu_id: str) -> None:
        """Удаление всех блюд подменю из кеша."""
        await self.cacher.delete(f'all_dishes_{submenu_id}')

    async def set_all_submenus_cache(self, menu_id: str,
                                     items: list[Submenu]) -> None:
        """Запись всех подменю в кеш."""
        await self.cacher.set(f'all_submenus_{menu_id}',
                              pickle.dumps(items), ex=EXPIRATION)

    async def get_all_submenus_cache(self,
                                     menu_id: str) -> list[Submenu] | None:
        """Получение всех подменю из кеша."""
        cache = await self.cacher.get(f'all_submenus_{menu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_submenu_cache(self, item: Submenu) -> None:
        """Запись подменю в кеш."""
        await self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    async def get_submenu_cache(self, id: str) -> Submenu | None:
        """Получение подменю из кеша."""
        cache = await self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при создании нового подменю."""
        await self.delete_menu_cache(str(item.menu_id))
        await self.delete_all_menu_cache()
        await self.delete_all_submenu_cache(str(item.menu_id))
        await self.set_submenu_cache(item)

    async def update_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при изменении подменю."""
        await self.delete_all_submenu_cache(str(item.menu_id))
        await self.set_submenu_cache(item)

    async def delete_submenu_cache(self, submenu_id: str,
                                   menu_id: str) -> None:
        """Работа с кэшем при удалении подменю."""
        await self.cacher.delete(submenu_id)
        await self.delete_all_dish_cache(submenu_id)
        await self.delete_all_submenu_cache(menu_id)
        dishes = await self.dish_repo.get_all_dishes(submenu_id)
        dish_ids = [str(dish.id) for dish in dishes]
        if dish_ids:
            await self.cacher.unlink(*dish_ids)
        await self.cacher.delete(menu_id)
        await self.delete_all_menu_cache()

    async def delete_all_submenu_cache(self, menu_id: str) -> None:
        """Удаление всех подменю меню из кеша."""
        await self.cacher.delete(f'all_submenus_{menu_id}')

    async def set_all_menus_cache(self, items: list[Menu]) -> None:
        """Запись всех меню в кеш."""
        await self.cacher.set('all_menus', pickle.dumps(items), ex=EXPIRATION)

    async def get_all_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кеша."""
        cache = await self.cacher.get('all_menus')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_full_base_menu_cache(self, items: list[Menu]) -> None:
        """Запись древовидной структуры базы в кэш."""
        await self.cacher.set('full_base_menu', pickle.dumps(items),
                              ex=EXPIRATION)

    async def get_full_base_menu_cache(self) -> list[Menu] | None:
        """Получение древовидной структуры базы из кеша."""
        cache = await self.cacher.get('full_base_menu')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_menu_cache(self, item: Menu) -> None:
        """Запись меню в кеш."""
        await self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    async def get_menu_cache(self, id: str) -> Menu | None:
        """Получение меню из кеша."""
        cache = await self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_update_menu_cache(self, item: Menu) -> None:
        """Работа с кэшем при создании нового меню."""
        await self.delete_all_menu_cache()
        await self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    async def delete_all_menu_cache(self) -> None:
        """Удаление всех меню из кеша."""
        await self.cacher.delete('all_menus')
        await self.cacher.delete('full_base_menu')

    async def delete_menu_cache(self, menu_id: str) -> None:
        """Работа с кэшем при удалении меню."""
        await self.cacher.delete(menu_id)
        await self.delete_all_menu_cache()
        await self.delete_all_submenu_cache(menu_id)
        submenus = await self.submenu_repo.get_all_submenus(menu_id)
        submenu_ids = [str(submenu.id) for submenu in submenus]
        if submenu_ids:
            await self.cacher.unlink(*submenu_ids)
