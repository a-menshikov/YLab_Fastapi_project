from fastapi import Depends

from app.api.submenus.crud_repository import SubmenuRepository
from app.database.cache_repository import СacheRepository
from app.database.schemas import SubmenuPost


class SubmenuService:
    """Сервисный репозиторий для подменю."""

    def __init__(self, crud_repo: SubmenuRepository = Depends(),
                 cache_repo: СacheRepository = Depends()) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    def get_all_submenus(self, menu_id: str):
        """Получение всех подменю."""
        cache = self.cache_repo.get_all_submenus_cache(menu_id)
        if not cache:
            items = self.crud_repo.get_all_submenus(menu_id=menu_id)
            self.cache_repo.set_all_submenus_cache(menu_id, items)
            return items
        return cache

    def get_submenu_by_id(self, id: str):
        """Получение подменю по id."""
        cache = self.cache_repo.get_submenu_cache(id)
        if not cache:
            item = self.crud_repo.get_submenu_by_id(id=id)
            self.cache_repo.set_submenu_cache(item)
            return item
        return cache

    def create_submenu(self, submenu: SubmenuPost, menu_id: str):
        """Добавление нового подменю."""
        item = self.crud_repo.create_submenu(submenu=submenu, menu_id=menu_id)
        self.cache_repo.create_submenu_cache(item)
        return item

    def update_submenu(self, submenu_id: str, updated_submenu: SubmenuPost):
        """Изменение подменю по id."""
        item = self.crud_repo.update_submenu(submenu_id=submenu_id,
                                             updated_submenu=updated_submenu)
        self.cache_repo.update_submenu_cache(item)
        return item

    def delete_submenu(self, menu_id: str, submenu_id: str):
        """Удаление подменю конкретного меню по id."""
        self.cache_repo.delete_submenu_cache(submenu_id)
        self.crud_repo.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
