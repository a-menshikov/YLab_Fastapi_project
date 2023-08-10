from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.database.db_loader import get_db
from app.database.models import Menu
from app.database.schemas import MenuPost
from app.database.services import check_unique_menu


class MenuRepository:
    """Репозиторий CRUD операций модели меню."""

    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db
        self.model = Menu

    async def get_menu_by_id(self, id: str) -> Menu:
        """Получение меню по id."""
        current_menu = (await self.db.execute(
            select(self.model).where(self.model.id == id)
        )).scalar()
        if not current_menu:
            raise NoResultFound('menu not found')
        return current_menu

    async def get_all_menus(self) -> list[Menu]:
        """Получение всех меню."""
        return (await self.db.execute(
            select(self.model)
        )).scalars().fetchall()

    async def create_menu(self, menu: MenuPost) -> Menu:
        """Добавление нового меню."""
        try:
            await check_unique_menu(db=self.db, menu=menu)
        except FlushError:
            raise FlushError('Меню с таким названием уже есть')
        db_menu = self.model(
            title=menu.title,
            description=menu.description,
        )
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        return db_menu

    async def update_menu(self, menu_id: str, updated_menu: MenuPost) -> Menu:
        """Изменение меню по id."""
        current_menu = await self.get_menu_by_id(id=menu_id)
        if not current_menu:
            raise NoResultFound('menu not found')
        try:
            await check_unique_menu(db=self.db, menu=updated_menu)
        except FlushError:
            raise FlushError('Меню с таким названием уже есть')
        current_menu.title = updated_menu.title
        current_menu.description = updated_menu.description
        self.db.merge(current_menu)
        await self.db.commit()
        await self.db.refresh(current_menu)
        return current_menu

    async def delete_menu(self, menu_id: str) -> None:
        """Удаление меню по id."""
        current_menu = await self.get_menu_by_id(id=menu_id)
        if not current_menu:
            raise NoResultFound('menu not found')
        await self.db.delete(current_menu)
        await self.db.commit()
