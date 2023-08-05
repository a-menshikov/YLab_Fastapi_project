from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.database.db_loader import get_db
from app.database.models import Menu
from app.database.schemas import MenuPost
from app.database.services import check_unique_menu


class MenuRepository:
    """Репозиторий CRUD операций модели меню."""

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.model = Menu

    def get_menu_by_id(self, id: str) -> Menu:
        """Получение меню по id."""
        current_menu = self.db.query(Menu).filter(Menu.id == id).first()
        if not current_menu:
            raise NoResultFound('menu not found')
        return self.db.query(Menu).filter(Menu.id == id).first()

    def get_all_menus(self) -> list[Menu]:
        """Получение всех меню."""
        return self.db.query(Menu).all()

    def create_menu(self, menu: MenuPost) -> Menu:
        """Добавление нового меню."""
        try:
            check_unique_menu(db=self.db, menu=menu)
        except FlushError:
            raise FlushError('Меню с таким названием уже есть')
        db_menu = Menu(
            title=menu.title,
            description=menu.description,
        )
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu

    def update_menu(self, menu_id: str, updated_menu: MenuPost) -> Menu:
        """Изменение меню по id."""
        current_menu = self.get_menu_by_id(id=menu_id)
        if not current_menu:
            raise NoResultFound('menu not found')
        try:
            check_unique_menu(db=self.db, menu=updated_menu)
        except FlushError:
            raise FlushError('Меню с таким названием уже есть')
        current_menu.title = updated_menu.title
        current_menu.description = updated_menu.description
        self.db.merge(current_menu)
        self.db.commit()
        self.db.refresh(current_menu)
        return current_menu

    def delete_menu(self, menu_id: str) -> None:
        """Удаление меню по id."""
        current_menu = self.get_menu_by_id(id=menu_id)
        if not current_menu:
            raise NoResultFound('menu not found')
        self.db.delete(current_menu)
        self.db.commit()
