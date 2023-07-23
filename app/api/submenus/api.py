from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.menus.crud import get_menu_by_id
from app.api.submenus.crud import (create_submenu, get_submenu_by_id,
                                   get_submenu_by_title, update_submenu)
from app.database.db_loader import get_db
from app.database.schemas import SubmenuPost, SubmenuRead

submenu_router = APIRouter(prefix="/api/v1/menus")


@submenu_router.get("/{menu_id}/submenus", response_model=SubmenuRead)
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    """Получение всех подменю конкретного меню."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    submenus = current_menu.submenus
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(submenus),
    )


@submenu_router.post("/{menu_id}/submenus", response_model=SubmenuRead)
def post_new_submenu(menu_id: str, submenu: SubmenuPost,
                     db: Session = Depends(get_db)):
    """Добавление нового подменю к конкретному меню."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    db_submenu = get_submenu_by_title(db, title=submenu.title, menu_id=menu_id)
    if db_submenu:
        raise HTTPException(
            status_code=400,
            detail="Подменю с таким title уже существует",
        )
    new_submenu = create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(new_submenu),
    )


@submenu_router.get("/{menu_id}/submenus/{submenu_id}",
                    response_model=SubmenuRead)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    """Получение подменю конкретного меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id, menu_id=menu_id)
    if not current_submenu:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(current_submenu),
    )


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}",
                      response_model=SubmenuRead)
def patch_submenu(menu_id: str, submenu_id: str, updated_submenu: SubmenuPost,
                  db: Session = Depends(get_db)):
    """Обновление подменю конкретного меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id, menu_id=menu_id)
    if not current_submenu:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(update_submenu(
            db,
            current_submenu,
            updated_submenu
        ))
    )


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str,
                   db: Session = Depends(get_db)):
    """Удаление подменю конкретного меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id, menu_id=menu_id)
    if not current_submenu:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    db.delete(current_submenu)
    db.commit()
    return JSONResponse(
        status_code=200,
        content='submenu deleted',
    )
