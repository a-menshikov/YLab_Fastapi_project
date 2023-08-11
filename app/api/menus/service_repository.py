from fastapi import Depends

from app.api.menus.crud_repository import MenuRepository
from app.database.cache_repository import СacheRepository
from app.database.models import Menu
from app.database.schemas import MenuPost


class MenuService:
    """Сервисный репозиторий для меню."""

    def __init__(self, crud_repo: MenuRepository = Depends(),
                 cache_repo: СacheRepository = Depends()):
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_menus(self) -> list[Menu]:
        """Получение всех меню."""
        cache = await self.cache_repo.get_all_menus_cache()
        if cache:
            return cache
        items = await self.crud_repo.get_all_menus()
        await self.cache_repo.set_all_menus_cache(items)
        return items

    async def get_menu_by_id(self, id: str) -> Menu:
        """Получение меню по id."""
        cache = await self.cache_repo.get_menu_cache(id)
        if cache:
            return cache
        item = await self.crud_repo.get_menu_by_id(id=id)
        await self.cache_repo.set_menu_cache(item)
        return item

    async def create_menu(self, menu: MenuPost) -> Menu:
        """Добавление нового меню."""
        item = await self.crud_repo.create_menu(menu=menu)
        await self.cache_repo.create_update_menu_cache(item)
        return item

    async def update_menu(self, menu_id: str, updated_menu: MenuPost) -> Menu:
        """Изменение меню по id."""
        item = await self.crud_repo.update_menu(menu_id=menu_id,
                                                updated_menu=updated_menu)
        await self.cache_repo.create_update_menu_cache(item)
        return item

    async def delete_menu(self, menu_id: str) -> None:
        """Удаление меню по id."""
        await self.cache_repo.delete_menu_cache(menu_id)
        await self.crud_repo.delete_menu(menu_id=menu_id)
