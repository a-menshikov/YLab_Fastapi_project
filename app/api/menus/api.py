from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.menus.crud import (create_menu, get_all_menus, get_menu_by_id,
                                get_menu_by_title, update_menu)
from app.database.db_loader import get_db
from app.database.schemas import MenuPost, MenuRead

menu_router = APIRouter(prefix="/api/v1")


@menu_router.get("/menus", response_model=MenuRead)
def get_menus(db: Session = Depends(get_db)):
    """Получение всех меню."""
    menus = get_all_menus(db)
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(menus)
    )


@menu_router.post("/menus", response_model=MenuRead)
def post_new_menu(menu: MenuPost, db: Session = Depends(get_db)):
    """Добавление нового меню."""
    db_menu = get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=400,
            detail="Меню с таким title уже существует",
        )
    new_menu = create_menu(db=db, menu=menu)
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(new_menu),
    )


@menu_router.get("/menus/{menu_id}", response_model=MenuRead)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    """Получение меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(current_menu),
    )


@menu_router.patch("/menus/{menu_id}", response_model=MenuRead)
def patch_menu(menu_id: str, updated_menu: MenuPost,
               db: Session = Depends(get_db)):
    """Изменение меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(update_menu(db, current_menu, updated_menu))
    )


@menu_router.delete("/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    """Удаление меню по id."""
    current_menu = get_menu_by_id(db=db, id=menu_id)
    if not current_menu:
        raise HTTPException(
            status_code=404,
            detail="menu not found",
        )
    db.delete(current_menu)
    db.commit()
    return JSONResponse(
        status_code=200,
        content='menu deleted',
    )
