import pickle

from fastapi import Depends
from redis import Redis

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

    def set_all_dishes_cache(self, submenu_id: str, items: list[Dish]) -> None:
        """Запись всех блюд в кеш."""
        self.cacher.set(f'all_dishes_{submenu_id}',
                        pickle.dumps(items), ex=EXPIRATION)

    def get_all_dishes_cache(self, submenu_id: str) -> list[Dish] | None:
        """Получение всех блюд из кеша."""
        cache = self.cacher.get(f'all_dishes_{submenu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_dish_cache(self, item: Dish) -> None:
        """Запись блюда в кеш."""
        self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_dish_cache(self, id: str) -> Dish | None:
        """Получение блюда из кеша."""
        cache = self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def delete_related_dish_cache(self, submenu_id: str, menu_id: str) -> None:
        """Удаление кэша связанных с блюдом объектов."""
        self.delete_all_dish_cache(submenu_id)
        self.cacher.delete(submenu_id)
        self.delete_all_submenu_cache(menu_id)
        self.cacher.delete(menu_id)
        self.delete_all_menu_cache()

    def create_dish_cache(self, item: Dish, submenu_id: str,
                          menu_id: str) -> None:
        """Работа с кэшем при создании нового блюда."""
        self.delete_related_dish_cache(submenu_id, menu_id)
        self.set_dish_cache(item)

    def update_dish_cache(self, item: Dish) -> None:
        """Работа с кэшем при изменении блюда."""
        self.delete_all_dish_cache(str(item.submenu_id))
        self.set_dish_cache(item)

    def delete_dish_cache(self, dish_id: str, submenu_id: str,
                          menu_id: str) -> None:
        """Работа с кэшем при удалении блюда."""
        self.cacher.delete(dish_id)
        self.delete_related_dish_cache(submenu_id, menu_id)

    def delete_all_dish_cache(self, submenu_id: str) -> None:
        """Удаление всех блюд подменю из кеша."""
        self.cacher.delete(f'all_dishes_{submenu_id}')

    def set_all_submenus_cache(self, menu_id: str,
                               items: list[Submenu]) -> None:
        """Запись всех подменю в кеш."""
        self.cacher.set(f'all_submenus_{menu_id}',
                        pickle.dumps(items), ex=EXPIRATION)

    def get_all_submenus_cache(self, menu_id: str) -> list[Submenu] | None:
        """Получение всех подменю из кеша."""
        cache = self.cacher.get(f'all_submenus_{menu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_submenu_cache(self, item: Submenu) -> None:
        """Запись подменю в кеш."""
        self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_submenu_cache(self, id: str) -> Submenu | None:
        """Получение подменю из кеша."""
        cache = self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def create_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при создании нового подменю."""
        self.delete_menu_cache(str(item.menu_id))
        self.delete_all_menu_cache()
        self.delete_all_submenu_cache(str(item.menu_id))
        self.set_submenu_cache(item)

    def update_submenu_cache(self, item: Submenu) -> None:
        """Работа с кэшем при изменении подменю."""
        self.delete_all_submenu_cache(str(item.menu_id))
        self.set_submenu_cache(item)

    def delete_submenu_cache(self, submenu_id: str, menu_id: str) -> None:
        """Работа с кэшем при удалении подменю."""
        self.cacher.delete(submenu_id)
        self.delete_all_dish_cache(submenu_id)
        self.delete_all_submenu_cache(menu_id)
        dishes = self.dish_repo.get_all_dishes(submenu_id)
        if dishes:
            for dish in dishes:
                self.delete_dish_cache(str(dish.id), submenu_id, menu_id)

    def delete_all_submenu_cache(self, menu_id: str) -> None:
        """Удаление всех подменю меню из кеша."""
        self.cacher.delete(f'all_submenus_{menu_id}')

    def set_all_menus_cache(self, items: list[Menu]) -> None:
        """Запись всех меню в кеш."""
        self.cacher.set('all_menus', pickle.dumps(items), ex=EXPIRATION)

    def get_all_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кеша."""
        cache = self.cacher.get('all_menus')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_menu_cache(self, item: Menu) -> None:
        """Запись меню в кеш."""
        self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_menu_cache(self, id: str) -> Menu | None:
        """Получение меню из кеша."""
        cache = self.cacher.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def create_update_menu_cache(self, item: Menu) -> None:
        """Работа с кэшем при создании нового меню."""
        self.delete_all_menu_cache()
        self.cacher.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def delete_all_menu_cache(self) -> None:
        """Удаление всех меню из кеша."""
        self.cacher.delete('all_menus')

    def delete_menu_cache(self, menu_id: str) -> None:
        """Работа с кэшем при удалении меню."""
        self.cacher.delete(menu_id)
        self.delete_all_menu_cache()
        self.delete_all_submenu_cache(menu_id)
        submenus = self.submenu_repo.get_all_submenus(menu_id)
        if submenus:
            for submenu in submenus:
                self.delete_submenu_cache(str(submenu.id), menu_id)
