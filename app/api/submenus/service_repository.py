from fastapi import Depends

from app.api.submenus.crud_repository import SubmenuRepository
from app.database.cache_repository import СacheRepository
from app.database.models import Submenu
from app.database.schemas import SubmenuPost


class SubmenuService:
    """Сервисный репозиторий для подменю."""

    def __init__(self, crud_repo: SubmenuRepository = Depends(),
                 cache_repo: СacheRepository = Depends()) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_submenus(self, menu_id: str) -> list[Submenu]:
        """Получение всех подменю."""
        cache = await self.cache_repo.get_all_submenus_cache(menu_id)
        if cache:
            return cache
        items = await self.crud_repo.get_all_submenus(menu_id=menu_id)
        await self.cache_repo.set_all_submenus_cache(menu_id, items)
        return items

    async def get_submenu_by_id(self, id: str, menu_id: str) -> Submenu:
        """Получение подменю по id."""
        cache = await self.cache_repo.get_submenu_cache(id, menu_id)
        if cache:
            return cache
        item = await self.crud_repo.get_submenu_by_id(id=id)
        await self.cache_repo.set_submenu_cache(item)
        return item

    async def create_submenu(self, submenu: SubmenuPost,
                             menu_id: str) -> Submenu:
        """Добавление нового подменю."""
        item = await self.crud_repo.create_submenu(submenu=submenu,
                                                   menu_id=menu_id)
        await self.cache_repo.create_submenu_cache(item)
        return item

    async def update_submenu(self, submenu_id: str,
                             updated_submenu: SubmenuPost) -> Submenu:
        """Изменение подменю по id."""
        item = await self.crud_repo.update_submenu(
            submenu_id=submenu_id,
            updated_submenu=updated_submenu,
        )
        await self.cache_repo.update_submenu_cache(item)
        return item

    async def delete_submenu(self, menu_id: str, submenu_id: str) -> None:
        """Удаление подменю конкретного меню по id."""
        await self.cache_repo.delete_submenu_cache(submenu_id=submenu_id,
                                                   menu_id=menu_id)
        await self.crud_repo.delete_submenu(menu_id=menu_id,
                                            submenu_id=submenu_id)
