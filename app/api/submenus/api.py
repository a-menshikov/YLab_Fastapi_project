from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.crud import get_menu_by_id
from app.api.submenus.crud import (create_submenu, get_submenu_by_id,
                                   update_submenu)
from app.database.db_loader import get_db
from app.database.schemas import SubmenuPost, SubmenuRead
from app.database.services import check_objects, check_unique_submenu

submenu_router = APIRouter(prefix="/api/v1/menus")


@submenu_router.get("/{menu_id}/submenus", response_model=List[SubmenuRead])
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    """Получение всех подменю конкретного меню."""
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_menu = get_menu_by_id(db=db, id=menu_id)
    return current_menu.submenus


@submenu_router.post("/{menu_id}/submenus", response_model=SubmenuRead,
                     status_code=201)
def post_new_submenu(menu_id: str, submenu: SubmenuPost,
                     db: Session = Depends(get_db)):
    """Добавление нового подменю к конкретному меню."""
    try:
        check_unique_submenu(db=db, submenu=submenu)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
    try:
        check_objects(db=db, menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    return create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@submenu_router.get("/{menu_id}/submenus/{submenu_id}",
                    response_model=SubmenuRead)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    """Получение подменю конкретного меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    return get_submenu_by_id(db=db, id=submenu_id)


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}",
                      response_model=SubmenuRead)
def patch_submenu(menu_id: str, submenu_id: str, updated_submenu: SubmenuPost,
                  db: Session = Depends(get_db)):
    """Обновление подменю конкретного меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    return update_submenu(db, current_submenu, updated_submenu)


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str,
                   db: Session = Depends(get_db)):
    """Удаление подменю конкретного меню по id."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    db.delete(current_submenu)
    db.commit()
    return JSONResponse(
        status_code=200,
        content='submenu deleted',
    )
