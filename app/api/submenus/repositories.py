from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.repositories import MenuRepository
from app.database.db_loader import get_db
from app.database.models import Submenu
from app.database.schemas import SubmenuPost
from app.database.services import check_objects, check_unique_submenu


class SubmenuRepository:
    """Репозиторий CRUD операций модели подменю."""

    def __init__(self, db: Session = Depends(get_db),
                 menu_repo: MenuRepository = Depends()) -> None:
        self.db = db
        self.menu_repo = menu_repo
        self.model = Submenu

    def create_submenu(self, submenu: SubmenuPost, menu_id: str):
        """Добавление нового подменю."""
        try:
            check_objects(db=self.db, menu_id=menu_id)
        except NoResultFound as error:
            raise NoResultFound(error.args[0])
        try:
            check_unique_submenu(db=self.db, submenu=submenu)
        except FlushError:
            raise FlushError('Подменю с таким названием уже есть')
        new_submenu = Submenu(
            title=submenu.title,
            description=submenu.description,
            menu_id=menu_id,
        )
        self.db.add(new_submenu)
        self.db.commit()
        self.db.refresh(new_submenu)
        return new_submenu

    def update_submenu(self, submenu_id: str, updated_submenu: SubmenuPost):
        """Изменение подменю по id."""
        current_submenu = self.get_submenu_by_id(id=submenu_id)
        if not current_submenu:
            raise NoResultFound('submenu not found')
        try:
            check_unique_submenu(db=self.db, submenu=updated_submenu)
        except FlushError:
            raise FlushError('Подменю с таким названием уже есть')
        current_submenu.title = updated_submenu.title
        current_submenu.description = updated_submenu.description
        self.db.merge(current_submenu)
        self.db.commit()
        self.db.refresh(current_submenu)
        return current_submenu

    def get_submenu_by_id(self, id: str):
        """Получение подменю по id."""
        current_submenu = self.db.query(Submenu).filter(
            Submenu.id == id,
        ).first()
        if not current_submenu:
            raise NoResultFound('submenu not found')
        return current_submenu

    def get_all_submenus(self, menu_id: str):
        """Получение всех подменю."""
        try:
            check_objects(db=self.db, menu_id=menu_id)
        except NoResultFound:
            return []
        else:
            current_menu = self.menu_repo.get_menu_by_id(id=menu_id)
            return current_menu.submenus

    def delete_submenu(self, menu_id: str, submenu_id: str):
        """Удаление подменю конкретного меню по id."""
        current_submenu = self.get_submenu_by_id(id=submenu_id)
        if not current_submenu:
            raise NoResultFound('submenu not found')
        self.db.delete(current_submenu)
        self.db.commit()


class SubmenuService:
    """Сервисный репозиторий для подменю."""

    def __init__(self, crud_repo: SubmenuRepository = Depends()):
        self.crud_repo = crud_repo

    def get_all_submenus(self, menu_id: str):
        """Получение всех подменю."""
        items = self.crud_repo.get_all_submenus(menu_id=menu_id)
        return items

    def get_submenu_by_id(self, id: str):
        """Получение подменю по id."""
        item = self.crud_repo.get_submenu_by_id(id=id)
        return item

    def create_submenu(self, submenu: SubmenuPost, menu_id: str):
        """Добавление нового подменю."""
        item = self.crud_repo.create_submenu(submenu=submenu, menu_id=menu_id)
        return item

    def update_submenu(self, submenu_id: str, updated_submenu: SubmenuPost):
        """Изменение подменю по id."""
        item = self.crud_repo.update_submenu(submenu_id=submenu_id,
                                             updated_submenu=updated_submenu)
        return item

    def delete_submenu(self, menu_id: str, submenu_id: str):
        """Удаление подменю конкретного меню по id."""
        self.crud_repo.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
