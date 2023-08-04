from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.dishes.crud import (
    create_dish,
    delete_dish,
    get_all_dishes,
    get_dish_by_id,
    update_dish,
)
from app.database.db_loader import get_db
from app.database.schemas import DishPost, DishRead

dish_router = APIRouter(prefix='/api/v1/menus')


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes',
                 response_model=list[DishRead])
def get_dishes(menu_id: str, submenu_id: str,
               db: Session = Depends(get_db)):
    """Получение всех блюд конкретного подменю."""
    return get_all_dishes(db=db, submenu_id=submenu_id)


@dish_router.post('/{menu_id}/submenus/{submenu_id}/dishes',
                  response_model=DishRead, status_code=201)
def post_new_dish(menu_id: str, submenu_id: str, dish: DishPost,
                  db: Session = Depends(get_db)):
    """Добавление нового блюда."""
    try:
        return create_dish(db=db, dish=dish, menu_id=menu_id,
                           submenu_id=submenu_id)
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


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                 response_model=DishRead)
def get_dish(menu_id: str, submenu_id: str, dish_id: str,
             db: Session = Depends(get_db)):
    """Получение блюда по id."""
    try:
        return get_dish_by_id(db=db, id=dish_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                   response_model=DishRead)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str,
               updated_dish: DishPost, db: Session = Depends(get_db)):
    """Изменение блюда по id."""
    try:
        return update_dish(db, dish_id, updated_dish)
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


@dish_router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def destroy_dish(menu_id: str, submenu_id: str, dish_id: str,
                 db: Session = Depends(get_db)):
    """Удаление блюда по id."""
    try:
        delete_dish(db=db, dish_id=dish_id)
        return JSONResponse(
            status_code=200,
            content='dish deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
