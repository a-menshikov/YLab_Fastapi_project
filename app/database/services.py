from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.database.models import Dish, Menu, Submenu
from app.database.schemas import DishPost, MenuPost, SubmenuPost


async def check_objects(db: AsyncSession, menu_id: str | None = None,
                        submenu_id: str | None = None,
                        dish_id: str | None = None) -> None:
    """Проверка на существование объектов"""
    if menu_id:
        query = select(exists().where(Menu.id == menu_id))
        exists_menu = await db.scalar(query)
        if not exists_menu:
            raise NoResultFound('menu not found')

    if submenu_id:
        query = select(exists().where(Submenu.id == submenu_id))
        exists_submenu = await db.scalar(query)
        if not exists_submenu:
            raise NoResultFound('submenu not found')

    if dish_id:
        query = select(exists().where(Dish.id == dish_id))
        exists_submenu = await db.scalar(query)
        if not exists_submenu:
            raise NoResultFound('dish not found')


async def check_unique_dish(db: AsyncSession, dish: DishPost) -> None:
    """Проверка на существование блюда."""
    query = select(exists().where(Dish.title == dish.title,
                                  Dish.description == dish.description))
    exists_dish = await db.scalar(query)
    if exists_dish:
        raise FlushError


async def check_unique_menu(db: AsyncSession, menu: MenuPost) -> None:
    """Проверка на существование меню."""
    query = select(exists().where(Menu.title == menu.title))
    exists_menu = await db.scalar(query)
    if exists_menu:
        raise FlushError


async def check_unique_submenu(db: AsyncSession, submenu: SubmenuPost) -> None:
    """Проверка на существование подменю."""
    query = select(exists().where(Submenu.title == submenu.title))
    exists_submenu = await db.scalar(query)
    if exists_submenu:
        raise FlushError
