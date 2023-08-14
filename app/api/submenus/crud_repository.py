from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.crud_repository import MenuRepository
from app.database.db_loader import get_db
from app.database.models import Submenu
from app.database.schemas import SubmenuPost
from app.database.services import check_objects, check_unique_submenu


class SubmenuRepository:
    """Репозиторий CRUD операций модели подменю."""

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        menu_repo: MenuRepository = Depends(),
    ) -> None:
        self.db = db
        self.menu_repo = menu_repo
        self.model = Submenu

    async def create_submenu(
        self,
        submenu: SubmenuPost,
        menu_id: str,
    ) -> Submenu:
        """Добавление нового подменю."""
        try:
            await check_objects(
                db=self.db,
                menu_id=menu_id,
            )
        except NoResultFound as error:
            raise NoResultFound(error.args[0])
        try:
            await check_unique_submenu(
                db=self.db,
                submenu=submenu,
            )
        except FlushError:
            raise FlushError('Подменю с такими параметрами уже есть')
        custom_id = submenu.id
        if custom_id:
            new_submenu = Submenu(
                id=custom_id,
                title=submenu.title,
                description=submenu.description,
                menu_id=menu_id,
            )
        else:
            new_submenu = Submenu(
                title=submenu.title,
                description=submenu.description,
                menu_id=menu_id,
            )
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def update_submenu(
        self,
        submenu_id: str,
        updated_submenu: SubmenuPost,
    ) -> Submenu:
        """Изменение подменю по id."""
        current_submenu = await self.get_submenu_by_id(id=submenu_id)
        if not current_submenu:
            raise NoResultFound('submenu not found')
        try:
            await check_unique_submenu(
                db=self.db,
                submenu=updated_submenu,
                submenu_id=submenu_id,
            )
        except FlushError:
            raise FlushError('Подменю с таким названием уже есть')
        current_submenu.title = updated_submenu.title
        current_submenu.description = updated_submenu.description
        await self.db.merge(current_submenu)
        await self.db.commit()
        await self.db.refresh(current_submenu)
        return current_submenu

    async def get_submenu_by_id(self, id: str) -> Submenu:
        """Получение подменю по id."""
        current_submenu = (await self.db.execute(
            select(self.model).where(self.model.id == id)
        )).scalar()
        if not current_submenu:
            raise NoResultFound('submenu not found')
        return current_submenu

    async def get_all_submenus(self, menu_id: str) -> list[Submenu]:
        """Получение всех подменю."""
        try:
            await check_objects(db=self.db, menu_id=menu_id)
        except NoResultFound:
            return []
        else:
            return ((await self.db.execute(
                select(self.model).where(self.model.menu_id == menu_id),
            )).scalars().all())

    async def delete_submenu(self, menu_id: str, submenu_id: str) -> None:
        """Удаление подменю конкретного меню по id."""
        current_submenu = await self.get_submenu_by_id(id=submenu_id)
        if not current_submenu:
            raise NoResultFound('submenu not found')
        await self.db.delete(current_submenu)
        await self.db.commit()
