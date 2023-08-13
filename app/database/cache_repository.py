import pickle

from aioredis import Redis
from fastapi import Depends

from app.config import (
    DISH_LINK,
    DISHES_LINK,
    EXPIRATION,
    MENU_LINK,
    MENUS_LINK,
    SUBMENU_LINK,
    SUBMENUS_LINK,
)
from app.database.db_loader import get_redis
from app.database.models import Dish, Menu, Submenu


class СacheRepository():
    """Сервисный репозиторий для кеширования объектов."""

    def __init__(self, cacher: Redis = Depends(get_redis)) -> None:
        self.cacher = cacher

    async def delete_cache_by_mask(self, pattern: str) -> None:
        """Удаление кэша по маске."""
        for key in await self.cacher.keys(pattern + '*'):
            await self.cacher.delete(key)

    async def set_all_dishes_cache(self, menu_id: str, submenu_id: str,
                                   items: list[Dish]) -> None:
        """Запись всех блюд в кеш."""
        await self.cacher.set(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id),
            pickle.dumps(items), ex=EXPIRATION
        )

    async def get_all_dishes_cache(self, menu_id: str,
                                   submenu_id: str) -> list[Dish] | None:
        """Получение всех блюд из кеша."""
        cache = await self.cacher.get(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id),
        )
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_dish_cache(self, item: Dish, submenu_id: str,
                             menu_id: str) -> None:
        """Запись блюда в кеш."""
        await self.cacher.set(
            DISH_LINK.format(menu_id=menu_id, submenu_id=submenu_id,
                             dish_id=str(item.id)),
            pickle.dumps(item),
            ex=EXPIRATION,
        )

    async def get_dish_cache(self, id: str, menu_id: str,
                             submenu_id: str) -> Dish | None:
        """Получение блюда из кеша."""
        cache = await self.cacher.get(
            DISH_LINK.format(menu_id=menu_id, submenu_id=submenu_id,
                             dish_id=id),
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_dish_cache(self, item: Dish, submenu_id: str,
                                menu_id: str) -> None:
        """Работа с кэшем при создании нового блюда."""
        await self.delete_cache_by_mask(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()
        await self.set_dish_cache(item=item, submenu_id=submenu_id,
                                  menu_id=menu_id)

    async def update_dish_cache(self, item: Dish, menu_id: str,
                                submenu_id: str) -> None:
        """Работа с кэшем при изменении блюда."""
        await self.delete_all_dish_cache(submenu_id, menu_id)
        await self.delete_full_base_cache()
        await self.set_dish_cache(item=item, submenu_id=submenu_id,
                                  menu_id=menu_id)

    async def delete_dish_cache(self, dish_id: str, submenu_id: str,
                                menu_id: str) -> None:
        """Работа с кэшем при удалении блюда."""
        await self.delete_cache_by_mask(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()

    async def delete_all_dish_cache(self, submenu_id: str,
                                    menu_id: str) -> None:
        """Удаление всех блюд подменю из кеша."""
        await self.cacher.delete(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id)
        )

    async def set_all_submenus_cache(self, menu_id: str,
                                     items: list[Submenu]) -> None:
        """Запись всех подменю в кеш."""
        await self.cacher.set(SUBMENUS_LINK.format(menu_id=menu_id),
                              pickle.dumps(items), ex=EXPIRATION)

    async def get_all_submenus_cache(self,
                                     menu_id: str) -> list[Submenu] | None:
        """Получение всех подменю из кеша."""
        cache = await self.cacher.get(SUBMENUS_LINK.format(menu_id=menu_id))
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_submenu_cache(self, item: Submenu) -> None:
        """Запись подменю в кеш."""
        await self.cacher.set(SUBMENU_LINK.format(
            menu_id=str(item.menu_id), submenu_id=str(item.id)
        ), pickle.dumps(item), ex=EXPIRATION)

    async def get_submenu_cache(self, id: str, menu_id: str) -> Submenu | None:
        """Получение подменю из кеша."""
        cache = await self.cacher.get(SUBMENU_LINK.format(
            menu_id=menu_id, submenu_id=id
        ))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при создании нового подменю."""
        await self.delete_cache_by_mask(
            MENU_LINK.format(menu_id=str(item.menu_id))
        )
        await self.delete_all_menu_cache()
        await self.set_submenu_cache(item)

    async def update_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при изменении подменю."""
        await self.delete_all_submenu_cache(str(item.menu_id))
        await self.delete_full_base_cache()
        await self.set_submenu_cache(item)

    async def delete_submenu_cache(self, submenu_id: str,
                                   menu_id: str) -> None:
        """Работа с кэшем при удалении подменю."""
        await self.delete_cache_by_mask(
            MENU_LINK.format(menu_id=menu_id)
        )
        await self.delete_all_menu_cache()

    async def delete_all_submenu_cache(self, menu_id: str) -> None:
        """Удаление всех подменю меню из кеша."""
        await self.cacher.delete(SUBMENUS_LINK.format(menu_id=menu_id))

    async def set_all_menus_cache(self, items: list[Menu]) -> None:
        """Запись всех меню в кеш."""
        await self.cacher.set(MENUS_LINK, pickle.dumps(items), ex=EXPIRATION)

    async def get_all_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кеша."""
        cache = await self.cacher.get(MENUS_LINK)
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
        await self.cacher.set(MENU_LINK.format(menu_id=str(item.id)),
                              pickle.dumps(item), ex=EXPIRATION)

    async def get_menu_cache(self, id: str) -> Menu | None:
        """Получение меню из кеша."""
        cache = await self.cacher.get(MENU_LINK.format(menu_id=id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_update_menu_cache(self, item: Menu) -> None:
        """Работа с кэшем при создании нового меню."""
        await self.delete_all_menu_cache()
        await self.cacher.set(MENU_LINK.format(menu_id=str(item.id)),
                              pickle.dumps(item), ex=EXPIRATION)

    async def delete_all_menu_cache(self) -> None:
        """Удаление всех меню из кеша."""
        await self.cacher.delete(MENUS_LINK)
        await self.delete_full_base_cache()

    async def delete_full_base_cache(self) -> None:
        """Удаление древовидной структуры базы из кеша."""
        await self.cacher.delete('full_base_menu')

    async def delete_menu_cache(self, menu_id: str) -> None:
        """Работа с кэшем при удалении меню."""
        await self.delete_cache_by_mask(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()
