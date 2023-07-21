from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.db_loader import get_db
from sqlalchemy.orm import Session
from app.database.schemas import MenuPost, MenuRead
from app.api.menus.crud import get_menu_by_title, create_menu, get_all_menus

menu_router = APIRouter(prefix="/api/v1")


@menu_router.get("/menus", response_model=MenuRead)
def get_menus(db: Session = Depends(get_db)):
    """Получение всех меню."""
    menus = get_all_menus(db)
    return JSONResponse(status_code=200, content=jsonable_encoder(menus))


@menu_router.post("/menus", response_model=MenuRead)
def post_new_menu(menu: MenuPost, db: Session = Depends(get_db)):
    """Добавление нового меню."""
    db_menu = get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(status_code=400,
                            detail="Меню с таким title уже существует")
    new_menu = create_menu(db=db, menu=menu)
    return JSONResponse(status_code=201, content=jsonable_encoder(new_menu))


@menu_router.get("/menus/{menu_id}")
def get_menu(menu_id: int):
    """Получение меню по id."""
    pass


@menu_router.patch("/menus/{menu_id}")
def patch_menu(menu_id: int):
    """Изменение меню по id."""
    pass


@menu_router.delete("/menus/{menu_id}")
def delete_menu(menu_id: int):
    """Удаление меню по id."""
    pass
