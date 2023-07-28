from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.crud import (create_submenu, delete_submenu,
                                   get_all_submenus, get_submenu_by_id,
                                   update_submenu)
from app.database.db_loader import get_db
from app.database.schemas import SubmenuPost, SubmenuRead

submenu_router = APIRouter(prefix="/api/v1/menus")


@submenu_router.get("/{menu_id}/submenus", response_model=List[SubmenuRead])
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    """Получение всех подменю конкретного меню."""
    return get_all_submenus(db=db, menu_id=menu_id)


@submenu_router.post("/{menu_id}/submenus", response_model=SubmenuRead,
                     status_code=201)
def post_new_submenu(menu_id: str, submenu: SubmenuPost,
                     db: Session = Depends(get_db)):
    """Добавление нового подменю к конкретному меню."""
    try:
        return create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@submenu_router.get("/{menu_id}/submenus/{submenu_id}",
                    response_model=SubmenuRead)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    """Получение подменю конкретного меню по id."""
    try:
        return get_submenu_by_id(db=db, id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}",
                      response_model=SubmenuRead)
def patch_submenu(menu_id: str, submenu_id: str, updated_submenu: SubmenuPost,
                  db: Session = Depends(get_db)):
    """Обновление подменю конкретного меню по id."""
    try:
        return update_submenu(db, submenu_id, updated_submenu)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}")
def destroy_submenu(menu_id: str, submenu_id: str,
                    db: Session = Depends(get_db)):
    """Удаление подменю конкретного меню по id."""
    try:
        delete_submenu(db, menu_id, submenu_id)
        return JSONResponse(
            status_code=200,
            content='submenu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
