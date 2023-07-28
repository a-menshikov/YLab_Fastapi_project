from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.crud import (create_menu, delete_menu, get_all_menus,
                                get_menu_by_id, update_menu)
from app.database.db_loader import get_db
from app.database.schemas import MenuPost, MenuRead
# from app.database.services import check_objects
menu_router = APIRouter(prefix="/api/v1")


@menu_router.get("/menus", response_model=List[MenuRead])
def get_menus(db: Session = Depends(get_db)):
    """Получение всех меню."""
    return get_all_menus(db)


@menu_router.post("/menus", response_model=MenuRead, status_code=201)
def post_new_menu(menu: MenuPost, db: Session = Depends(get_db)):
    """Добавление нового меню."""
    try:
        return create_menu(db=db, menu=menu)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@menu_router.get("/menus/{menu_id}", response_model=MenuRead)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    """Получение меню по id."""
    try:
        return get_menu_by_id(db=db, id=menu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@menu_router.patch("/menus/{menu_id}", response_model=MenuRead)
def patch_menu(menu_id: str, updated_menu: MenuPost,
               db: Session = Depends(get_db)):
    """Изменение меню по id."""
    try:
        return update_menu(db, menu_id, updated_menu)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@menu_router.delete("/menus/{menu_id}")
def destroy_menu(menu_id: str, db: Session = Depends(get_db)):
    """Удаление меню по id."""
    try:
        delete_menu(db=db, menu_id=menu_id)
        return JSONResponse(
            status_code=200,
            content='menu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
