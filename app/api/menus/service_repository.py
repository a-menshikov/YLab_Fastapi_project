from fastapi import Depends

from app.api.menus.crud_repository import MenuRepository
from app.database.cache_repository import СacheRepository
from app.database.schemas import MenuPost


class MenuService:
    """Сервисный репозиторий для меню."""

    def __init__(self, crud_repo: MenuRepository = Depends(),
                 cache_repo: СacheRepository = Depends()):
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    def get_all_menus(self):
        """Получение всех меню."""
        cache = self.cache_repo.get_all_menus_cache()
        if not cache:
            items = self.crud_repo.get_all_menus()
            self.cache_repo.set_all_menus_cache(items)
            return items
        return cache

    def get_menu_by_id(self, id: str):
        """Получение меню по id."""
        cache = self.cache_repo.get_menu_cache(id)
        if not cache:
            item = self.crud_repo.get_menu_by_id(id=id)
            self.cache_repo.set_menu_cache(item)
            return item
        return cache

    def create_menu(self, menu: MenuPost):
        """Добавление нового меню."""
        item = self.crud_repo.create_menu(menu=menu)
        self.cache_repo.create_update_menu_cache(item)
        return item

    def update_menu(self, menu_id: str, updated_menu: MenuPost):
        """Изменение меню по id."""
        item = self.crud_repo.update_menu(menu_id=menu_id,
                                          updated_menu=updated_menu)
        self.cache_repo.create_update_menu_cache(item)
        return item

    def delete_menu(self, menu_id: str):
        """Удаление меню по id."""
        self.cache_repo.delete_menu_cache(menu_id)
        self.crud_repo.delete_menu(menu_id=menu_id)
